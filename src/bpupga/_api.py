"""Thin wrappers around existing implementations; no campaign files are changed.

This in-process interface is not the benchmark's sealed subprocess executor.
Labels belong to data construction and post-inference evaluation, never align().
"""
from __future__ import annotations

import copy
import contextlib
import importlib
import json
import random
import sys
from argparse import Namespace
from dataclasses import dataclass, replace
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Mapping, Sequence

import networkx as nx
import numpy as np

# The public facade lives under api/; its frozen research dependencies remain
# at the dated project root, outside the API source directory.
_ROOT = Path(__file__).resolve().parents[2]
_BASELINE = _ROOT / "baseline"
# Existing adapters use the top-level common contract. Do not load a second
# baseline.common contract, or isinstance checks cease to mean the same thing.
for _name in ("baseline", "baselines", "common", "common.dataset", "common.result"):
    _loaded = sys.modules.get(_name)
    if _loaded is not None and getattr(_loaded, "__file__", None):
        if not Path(_loaded.__file__).resolve().is_relative_to(_BASELINE):
            raise ImportError(f"{_name} is already loaded from another checkout; use a fresh Python process")
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
import baseline  # noqa: E402 -- establishes the existing common import path
from common.dataset import AlignmentDataset, load_dataset  # noqa: E402
from common.result import AlignmentResult  # noqa: E402

_BUILTINS = frozenset((
    "alpine", "cena", "fugal", "gradalign_plus", "grampa", "immnc",
    "oiteralign", "opgm_unsupervised", "regal", "s_gwl", "slotalign", "ulot",
))
_CUSTOM: dict[str, Callable[..., Any]] = {}


def _private_package(name: str, directory: Path) -> str:
    """Load relative modules without colliding with top-level evaluation."""
    if name not in sys.modules:
        package = ModuleType(name)
        package.__path__ = [str(directory)]
        package.__package__ = name
        sys.modules[name] = package
    return name


def _metrics():
    package = _private_package("bpupga._native_runtime", _ROOT / "evaluation/runtime")
    return importlib.import_module(package + ".metrics")


class Dataset:
    """Load G1/G2 edge lists, optional node lists, Alignment.json and metadata.

    Original integer IDs are mapped to contiguous local IDs. Explicit node
    files preserve isolates; the returned AlignmentDataset retains both maps.
    """

    @staticmethod
    def load(root: str | Path) -> AlignmentDataset:
        return load_dataset(root)


def construct(
    root: str | Path,
    *,
    rho_source: float,
    rho_target: float,
    construction_seed: int = 2026,
    output_dir: str | Path,
) -> AlignmentDataset:
    """Materialize the existing bilateral partial-overlap construction.

    root contains the raw G1/G2 files and Alignment.json. The constructor
    partitions known matched identities into shared/source-only/target-only
    groups and excludes pre-existing unmatched identities. Ratios are node
    overlap requests, with finite-size rounding recorded in metadata. Existing
    outputs are never replaced, including dangling symbolic links.
    """
    from date_261023.construct_bilateral_partial import (
        construct_dataset, load_raw_dataset, write_constructed_dataset,
    )

    source = Path(root).expanduser().resolve()
    destination = Path(output_dir).expanduser().absolute()
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"Output already exists: {destination}")
    args = Namespace(
        raw_dir_name=".", g1_file="G1.edgelist", g2_file="G2.edgelist",
        g1_nodes_file="G1.nodes", g2_nodes_file="G2.nodes",
        alignment_file="Alignment.json",
    )
    raw = load_raw_dataset(source.parent, source.name, args)
    built = construct_dataset(
        raw, rho_source, rho_target, construction_seed,
        raw_dir_relative=str(source),
    )
    write_constructed_dataset(destination, built, force=False)
    return load_dataset(destination)


def register_algorithm(name: str, factory: Callable[..., Any]) -> None:
    """Register a new name without replacing a built-in or existing adapter.

    factory(parameters=..., seed=..., device=..., dataset_family=...) returns
    an object with fit(graph1, graph2) -> AlignmentResult. The factory never
    receives a Dataset. Custom code must preserve the unsupervised contract.
    """
    if not isinstance(name, str) or not name or name.strip() != name:
        raise ValueError("Algorithm name must be a nonempty, trimmed string")
    if name in _BUILTINS or name == "opgm" or name in _CUSTOM:
        raise ValueError(f"Algorithm name is already reserved: {name}")
    if not callable(factory):
        raise TypeError("factory must be callable")
    _CUSTOM[name] = factory


def _topology(graph: nx.Graph) -> nx.Graph:
    if not isinstance(graph, nx.Graph) or graph.is_directed() or graph.is_multigraph():
        raise TypeError("align requires simple undirected NetworkX graphs")
    if not len(graph) or set(graph) != set(range(len(graph))):
        raise ValueError("Use nonempty graphs with contiguous local IDs 0..n-1; Dataset.load performs reindexing")
    if nx.number_of_selfloops(graph):
        raise ValueError("align requires graphs without self loops")
    # Discard graph, node and edge attributes, including any caller annotations.
    clean = nx.Graph()
    clean.add_nodes_from(range(len(graph)))
    clean.add_edges_from(graph.edges())
    # Match the existing graph packet: seeded random walks can depend on
    # adjacency iteration order even when the mathematical graph is identical.
    for node in clean:
        clean._adj[node] = {neighbor: clean._adj[node][neighbor] for neighbor in graph.neighbors(node)}
    return clean


class Algorithm:
    """Configure an adapter, then call align(graph1, graph2).

    The default device is CPU. Built-in adapter/config defaults apply; this
    does not silently import a frozen campaign's family-specific parameters.
    Registry construction is lazy and exceptions propagate to the caller.
    """

    def __init__(self, method: str, parameters: Mapping[str, Any] | None = None,
                 *, seed: int = 2026, device: str = "cpu", dataset_family: str = ""):
        if method == "opgm":
            raise ValueError("Supervised OPGM-rs is protocol-incompatible; use the explicitly changed opgm_unsupervised adapter")
        if method not in _BUILTINS and method not in _CUSTOM:
            raise ValueError(f"Unknown algorithm {method!r}; built-ins: {', '.join(sorted(_BUILTINS))}")
        if method == "alpine" and device not in {"cpu", "auto"}:
            raise ValueError("The original-author ALPINE adapter supports CPU only; use device='cpu' or 'auto'")
        self.method, self.parameters = method, copy.deepcopy(dict(parameters or {}))
        forbidden = {"ground_truth", "gt", "true_k", "true_K", "true_overlap", "dataset", "data_root"}
        if forbidden.intersection(self.parameters):
            raise ValueError("Ground truth, true cardinality/overlap and dataset inputs are forbidden parameters")
        self.seed, self.device, self.dataset_family = seed, device, dataset_family
        self.config: dict[str, Any] | None = None

    def align(self, graph1: nx.Graph, graph2: nx.Graph) -> AlignmentResult:
        graphs = (_topology(graph1), _topology(graph2))
        input_sizes = tuple(map(len, graphs))
        random.seed(self.seed)
        np.random.seed(self.seed)
        parameters = copy.deepcopy(self.parameters)
        if self.method in _CUSTOM:
            model = _CUSTOM[self.method](parameters=parameters, seed=self.seed,
                                         device=self.device, dataset_family=self.dataset_family)
            self.config = parameters
        else:
            # Importing a built-in registry may require the project's model
            # environment; custom adapters do not acquire that dependency.
            import torch
            torch.manual_seed(self.seed)
            if self.method == "opgm_unsupervised":
                from baseline.opgm_unsupervised.model import construct as make_model
                model, self.config = make_model(parameters, self.seed, self.device)
            elif self.method == "alpine":
                from baseline.alpine_author_cpu import AuthorCPUAlpine
                defaults = dict(mu=1.0, niter=10, inner_iterations=10, weight=2,
                                sinkhorn_reg=1.0, sinkhorn_iterations=500,
                                sinkhorn_tolerance=1e-5, dtype="float64", device="cpu")
                unsupported = parameters.keys() - defaults.keys()
                if unsupported:
                    raise TypeError(f"Unsupported original-author ALPINE parameters: {', '.join(sorted(unsupported))}")
                if parameters.get("device", "cpu") not in {"cpu", "auto"}:
                    raise ValueError("The original-author ALPINE adapter supports CPU only")
                self.config = dict(defaults, **parameters)
                self.config.update(device="cpu", implementation="original_author_CPU_261030")
                if self.config["niter"] != 10:
                    raise ValueError("The original ALPINE code fixes ten outer iterations; niter must be 10")
                if self.config["mu"] < 0 or self.config["weight"] not in {1, 2}:
                    raise ValueError("ALPINE requires nonnegative mu and weight in {1, 2}")
                model = AuthorCPUAlpine(self.config)
            else:
                from baseline.registry import construct as make_model
                model, self.config = make_model(self.method, parameters, self.seed, self.device, self.dataset_family)
        if not callable(getattr(model, "fit", None)):
            raise TypeError("Algorithm factory must return an adapter with fit(graph1, graph2)")
        context = contextlib.nullcontext()
        if self.method == "s_gwl":
            from baseline.sgwl_numerics_v2 import stable_proximal_state
            context = stable_proximal_state()
        with context as numerical:
            result = model.fit(*graphs)
        if numerical is not None:
            result.metadata["numerical_revision"] = "retained_log_proximal_state_and_dual_gauge_v2"
            result.metadata["numerical_revision_diagnostics"] = dict(numerical)
        _validate_result(result, *input_sizes)
        return result


def _validate_result(result: AlignmentResult, n1: int, n2: int) -> dict[str, Any]:
    if not isinstance(result, AlignmentResult):
        raise TypeError("Expected bpupga.AlignmentResult")
    result.validate_shapes(n1, n2)
    validity = _metrics().validate_predicted_pairs(result.predicted_pairs, n1, n2)
    if validity["out_of_range_count"]:
        raise ValueError("Result contains out-of-range predicted pairs")
    if result.metadata.get("nonfinite_guard_triggered"):
        raise FloatingPointError("Adapter reported a nonfinite guard; no successful score is returned")
    for field in ("score_matrix", "cost_matrix", "source_embeddings", "target_embeddings"):
        value = getattr(result, field)
        if value is not None and not np.isfinite(value).all():
            raise FloatingPointError(f"Non-finite {field}")
    return validity


def _validate_ks(ks: Sequence[int]) -> tuple[int, ...]:
    values = tuple(ks)
    if not values or any(not isinstance(k, int) or isinstance(k, bool) or k < 1 for k in values):
        raise ValueError("ks must contain positive integers")
    return values


def _reference_note(dataset: AlignmentDataset) -> str:
    note = ("Scores and private-node labels are relative to the supplied reference. "
            "An unannotated node is not established as truly unmatched when the reference is incomplete.")
    limitation = _reference_limitation(dataset)
    return note + (" " + limitation if limitation else "")


def _reference_limitation(dataset: AlignmentDataset) -> str | None:
    metadata = dataset.metadata
    if metadata.get("groundtruth_limitations"):
        return str(metadata["groundtruth_limitations"])
    if metadata.get("ground_truth_complete") is False or metadata.get("groundtruth_complete") is False:
        return "Dataset metadata declares the reference incomplete."
    return None


def evaluate(result: AlignmentResult, dataset: AlignmentDataset,
             *, ks: Sequence[int] = (1, 5, 10)) -> dict[str, Any]:
    """Score native pairs and available same-fit rankings after inference.

    Pair scoring removes exact duplicate pairs and reports endpoint conflicts.
    Node classification additionally reports accuracy, balanced accuracy and
    unmatched-node scores for complete references. No decoder or refit is run.
    Rankings cover reference-matched queries and
    do not establish rejection quality. GRAMPA uses the current soft transform
    and also exposes its raw ranking; sparse candidates are not densified.
    """
    ks = _validate_ks(ks)
    m = _metrics()
    n1, n2 = len(dataset.graph1), len(dataset.graph2)
    validity = _validate_result(result, n1, n2)
    truth = dataset.ground_truth
    reverse = {v: u for u, v in truth.items()}
    report = {
        "method": result.method, "output_variant": "native",
        "pair": m.evaluate_pair_set(result.predicted_pairs, truth, n1, n2),
        "matchability": m.evaluate_matchability(result.predicted_pairs, truth, n1, n2),
        "overlap_estimation": m.evaluate_overlap_estimation(result.predicted_pairs, truth, n1, n2),
        "validity": validity, "reference_note": _reference_note(dataset),
        "runtime": {"native_reported_seconds": result.runtime_sec,
                    "peak_memory_mb": result.peak_memory_mb},
    }
    report["node_classification"] = None
    if _reference_limitation(dataset):
        report["matchability"] = None
        report["overlap_estimation"] = None
        report["node_classification"] = None
        report["skipped_metrics"] = {
            "matchability": "Incomplete reference cannot identify all truly unmatched nodes",
            "overlap_estimation": "Incomplete reference does not establish true overlap size",
            "node_classification": "Incomplete reference cannot define matched/unmatched confusion counts",
        }
    else:
        runtime = _private_package("bpupga._native_runtime", _ROOT / "evaluation/runtime")
        classification = importlib.import_module(runtime + ".evaluate").node_classification
        report["node_classification"] = classification(result.predicted_pairs, truth, n1, n2)

    def directions(forward, backward):
        return {"source_to_target": forward, "target_to_source": backward,
                "bidirectional": {key: (forward[key] + backward[key]) / 2
                                   for key in (*[f"hits@{k}" for k in ks], "mrr")}}

    quality = None
    if result.score_matrix is not None:
        quality = np.asarray(result.score_matrix)
        if result.larger_is_better is False:
            quality = -quality
        representation = "score_matrix"
    elif result.cost_matrix is not None:
        quality = -np.asarray(result.cost_matrix)
        representation = "negative_cost_matrix"
    if quality is not None:
        def matrix_ranking(matrix):
            return directions(m.evaluate_ranking_from_matrix(matrix, truth, ks),
                              m.evaluate_ranking_from_matrix(matrix.T, reverse, ks))
        report["ranking"] = matrix_ranking(quality)
        report["ranking_policy"] = {"representation": representation,
                                    "queries": "reference-matched nodes only",
                                    "tie_break": "lower local candidate ID"}
        if result.method.lower() == "grampa":
            package = _private_package("bpupga._native_runtime", _ROOT / "evaluation/runtime")
            soft = importlib.import_module(package + ".grampa_soft_ranking")
            report["raw_ranking"] = report["ranking"]
            report["ranking"] = matrix_ranking(soft.sinkhorn_soft_scores(quality))
            report["ranking_policy"].update(soft.POLICY)
    elif result.ranking_candidates is not None:
        candidates = result.ranking_candidates
        report["ranking"] = directions(
            m.evaluate_ranking_from_candidates(candidates, truth, ks),
            m.evaluate_ranking_from_candidates(((v, u, s) for u, v, s in candidates), reverse, ks))
        report["ranking_policy"] = {"representation": "sparse_native_candidates",
                                    "missing_reference_pair": "zero reciprocal rank"}
    elif result.source_embeddings is not None and result.target_embeddings is not None:
        source, target = result.source_embeddings, result.target_embeddings
        report["ranking"] = directions(
            m.evaluate_ranking_from_embeddings(source, target, truth, ks),
            m.evaluate_ranking_from_embeddings(target, source, reverse, ks))
        report["ranking_policy"] = {"representation": "euclidean_embedding_distance"}
    else:
        report["ranking"] = None
        report["ranking_policy"] = {"skipped_reason": "No same-fit scores, candidates or paired embeddings"}
    return report


def diagnose(result: AlignmentResult, dataset: AlignmentDataset,
             *, ks: Sequence[int] = (1, 5, 10), example_limit: int = 10,
             max_dense_entries: int = 25_000_000) -> dict[str, Any]:
    """Run the existing evaluation-only diagnostic module without saving files.

    Requires BPUPGA/baseline261023/evaluation from the research checkout.
    Endpoint-mask oracle comparisons are explicitly labeled in the report;
    true-cardinality oracle decoding remains disabled. No result is refitted.
    """
    ks = _validate_ks(ks)
    if example_limit < 0 or max_dense_entries < 1:
        raise ValueError("example_limit must be nonnegative and max_dense_entries positive")
    n1, n2 = len(dataset.graph1), len(dataset.graph2)
    validity = _validate_result(result, n1, n2)
    if _reference_limitation(dataset):
        return {
            "schema_version": 1, "method": result.method,
            "native_output": {"pair": _metrics().evaluate_pair_set(result.predicted_pairs, dataset.ground_truth, n1, n2),
                              "validity": validity},
            "score_space": {"available": False, "skipped_reason": "Incomplete ground-truth reference"},
            "skipped_diagnostics": {
                "private_node_error_decomposition": "Unannotated nodes are not known private nodes",
                "matchability_signal": "Incomplete reference cannot label true matchability",
                "oracle_decoding_ladder": "Reference overlap masks and cardinality are incomplete",
            },
            "reference_note": _reference_note(dataset),
            "leakage_statement": "Post-inference reference accounting only; no refit or oracle decoding",
        }
    legacy = _ROOT.parent / "BPUPGA/baseline261023/evaluation"
    if not (legacy / "diagnostics.py").is_file():
        raise FileNotFoundError(f"Optional diagnostic source is absent: {legacy / 'diagnostics.py'}")
    package = _private_package("bpupga._legacy_evaluation", legacy)
    module = importlib.import_module(package + ".diagnostics")
    # Legacy diagnostics interprets score_matrix as quality regardless of the
    # direction flag. Normalize a shallow dataclass copy, never mutate result.
    diagnostic_result = result
    if result.score_matrix is not None and result.larger_is_better is False:
        diagnostic_result = replace(result, score_matrix=-np.asarray(result.score_matrix), larger_is_better=True)
    report = module.diagnose_alignment_result(
        diagnostic_result, dataset, ks=ks, example_limit=example_limit,
        max_dense_entries=max_dense_entries, include_oracle_k=False,
    )
    report["reference_note"] = _reference_note(dataset)
    return report


@dataclass(frozen=True)
class RunLog:
    """Read an existing attempt's current result.json or started.json snapshot.

    Does not scan matrices, rerun inference, write, watch or update a campaign.
    Failure/running scores are None, never successful zeroes.
    """

    attempt_dir: Path
    _record: dict[str, Any]
    _failure: dict[str, Any] | None = None

    @classmethod
    def open(cls, attempt_dir: str | Path) -> "RunLog":
        root = Path(attempt_dir).expanduser().resolve()
        result = root / "result.json"
        if not result.is_file():
            result = root / "started.json"
        record = _read_object(result)
        if not isinstance(record.get("status"), str):
            raise ValueError(f"Missing string status in {result}")
        failure = root / "fit_failure.json"
        return cls(root, record, _read_object(failure) if failure.is_file() else None)

    @property
    def status(self) -> str:
        return self._record["status"]

    @property
    def native_metrics(self) -> dict[str, Any] | None:
        if self.status != "SUCCESS":
            return None
        return copy.deepcopy(self._record.get("variants", {}).get("native"))

    @property
    def runtime(self) -> dict[str, Any]:
        runtime = copy.deepcopy(self._record.get("runtime", {}))
        if "end_to_end_seconds" in self._record:
            runtime.setdefault("end_to_end_seconds", self._record["end_to_end_seconds"])
        return runtime

    @property
    def errors(self) -> list[dict[str, Any]]:
        errors = []
        if self._record.get("error"):
            errors.append({key: self._record[key] for key in ("status", "error", "traceback") if key in self._record})
        if self._failure:
            errors.append(copy.deepcopy(self._failure))
        return errors

    def summary(self) -> dict[str, Any]:
        return {"attempt_dir": str(self.attempt_dir), "status": self.status,
                "task": copy.deepcopy(self._record.get("task", {})),
                "native_metrics": self.native_metrics, "runtime": self.runtime,
                "errors": self.errors}


def _read_object(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value
