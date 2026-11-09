[Repository home](../README.md) · [Documentation index](documentation-index.md) · [← Custom algorithms](extending.md) · [Troubleshooting →](faq.md)

# Python API reference

Signatures, parameters, return fields, exceptions and examples for the exported BPUPGA interface.

This reference describes the exported repository-local Python interface. Import it with `import bpupga as bp` after following the [installation guide](installation.md). Examples using `data`, `result`, or `instance_root` continue from the [quickstart](quickstart.md).

[Dataset.load](#section-dataset-load) · [construct](#section-construct) · [Algorithm](#section-algorithm) · [align](#section-algorithm-align) · [AlignmentDataset](#section-alignmentdataset) · [AlignmentResult](#section-alignmentresult) · [evaluate](#section-evaluate) · [diagnose](#section-diagnose) · [RunLog.open](#section-runlog-open) · [register\_algorithm](#section-register-algorithm)

<a name="section-dataset-load"></a>

<a name="section-dataset-load-2"></a>

## Dataset.load

[source](../src/bpupga/_api.py#L70)

```python
Dataset.load(root: str | Path) -> AlignmentDataset
```

Load a prepared pair from its files, normalize simple undirected topology, and map sorted original integer node IDs to consecutive local IDs.

<a name="section-parameters"></a>

### Parameters

| Name | Type / default | Description |
| --- | --- | --- |
| root | str \| pathlib.Path; required | Prepared directory with G1.edgelist, G2.edgelist, and Alignment.json; optional G1.nodes, G2.nodes, metadata.json. |

<a name="section-returns"></a>

### Returns

An [AlignmentDataset](#section-alignmentdataset). Explicit node files preserve isolates, self loops are removed, and the reference is validated as an injective mapping within the loaded graph membership.

<a name="section-raises"></a>

### Raises

`NotADirectoryError` for a missing dataset directory; `FileNotFoundError` for required files; `ValueError` for malformed graph/reference data or inconsistent declared overlap metadata. JSON and integer-parsing errors propagate from the loader.

**Python**

```python
data = bp.Dataset.load(instance_root)
print(data.summary())
```

See [datasets and construction](datasets.md).

<a name="section-construct"></a>

<a name="section-construct-2"></a>

## construct

[source](../src/bpupga/_api.py#L74)

```python
construct(root, *, rho_source, rho_target, construction_seed=2026, output_dir) -> AlignmentDataset
```

Wrap the existing bilateral partition-pool constructor, write a new instance, and load the result through the shared dataset interface.

<a name="section-parameters-2"></a>

### Parameters

| Name | Type / default | Description |
| --- | --- | --- |
| root | str \| Path; required | Raw graph-pair directory with integer-ID G1/G2 edge files and Alignment.json. |
| rho\_source | float; required keyword | Requested source node overlap in (0, 1\]. |
| rho\_target | float; required keyword | Requested target node overlap in (0, 1\]. |
| construction\_seed | int = 2026 | Seed controlling matched-identity partition construction. |
| output\_dir | str \| Path; required keyword | New output directory; existing paths and symlinks are refused. |

<a name="section-returns-2"></a>

### Returns

An [AlignmentDataset](#section-alignmentdataset) with the generated files, requested/realized overlap and construction provenance.

<a name="section-notes"></a>

### Notes

The controlled pool contains known matched identities. Preexisting unmatched nodes are excluded; retained edges are induced from the selected endpoint sets. The constructor retains original IDs, while loading maps each side to local consecutive IDs. This is node-overlap construction, not an edge-deletion-noise control.

<a name="section-raises-2"></a>

### Raises

`FileExistsError` if the destination exists; `ValueError` for invalid ratios, infeasible allocation, or malformed inputs; loader and file-system errors propagate.

**Python**

```python
data = bp.construct(
    raw_root, rho_source=0.8, rho_target=0.6,
    construction_seed=2026, output_dir="runs/new_instance",
)
```

<a name="section-algorithm"></a>

<a name="section-algorithm-2"></a>

## Algorithm

[source](../src/bpupga/_api.py#L146)

```python
Algorithm(method, parameters=None, *, seed=2026, device='cpu', dataset_family='')
```

Configure a named built-in or registered custom adapter. Model construction is lazy and takes place in [align](#section-algorithm-align).

<a name="section-parameters-3"></a>

### Parameters

| Name | Type / default | Description |
| --- | --- | --- |
| method | str; required | A current built-in name or a registered custom name. |
| parameters | Mapping\[str, Any\] \| None = None | Method-specific constructor parameters; copied by the facade. |
| seed | int = 2026 | Execution seed passed to the adapter. |
| device | str = 'cpu' | Requested device, subject to the implementation's support. |
| dataset\_family | str = '' | Existing FUGAL family-specific numerical policy; use 'Oregon-1' where appropriate. |

<a name="section-attributes"></a>

### Attributes

`method`, `parameters`, `seed`, `device`, and `dataset_family` retain the configuration. `config` is `None` before model construction and holds the resulting configuration after construction during alignment.

<a name="section-raises-3"></a>

### Raises

`ValueError` for unknown or supervised `opgm` names, prohibited reference-bearing parameter keys, or an explicit non-CPU ALPINE device. ALPINE's fixed author controls and other method-specific parameters are checked during alignment.

**Python**

```python
algorithm = bp.Algorithm(
    "grampa", {"eta": 1.0}, seed=2026, device="cpu")
```

See [method names and parameter excerpts](algorithms.md).

<a name="section-algorithm-align"></a>

<a name="section-algorithm-align-2"></a>

## Algorithm.align

[source](../src/bpupga/_api.py#L169)

```python
Algorithm.align(graph1: nx.Graph, graph2: nx.Graph) -> AlignmentResult
```

Copy the two input topologies, discard graph/node/edge attributes, construct the adapter, and call its internal graph-only computation. Original caller graphs are not passed for mutation.

<a name="section-parameters-4"></a>

### Parameters

| Name | Requirement |
| --- | --- |
| graph1 | Nonempty simple undirected NetworkX graph, no self loops, IDs 0..n\_source-1. |
| graph2 | Nonempty simple undirected NetworkX graph, no self loops, IDs 0..n\_target-1. |

<a name="section-returns-3"></a>

### Returns

An [AlignmentResult](#section-alignmentresult) with native local-ID pairs and available method outputs. Neighbor iteration order is preserved by the topology copies.

<a name="section-raises-4"></a>

### Raises

`TypeError` for unsupported graph types, invalid custom adapters or result types; `ValueError` for incompatible IDs, self loops, result shapes or out-of-range pairs; `FloatingPointError` for validated nonfinite matrix/embedding outputs or a reported nonfinite guard. Method construction and execution errors propagate.

<a name="section-notes-2"></a>

### Notes

No dataset, reference mapping, true cardinality, or true overlap is an alignment argument. The facade runs in the caller process; formal campaign resource allocation and subprocess sealing are separate.

**Python**

```python
result = algorithm.align(data.graph1, data.graph2)
original_pairs = data.pairs_to_original(result.predicted_pairs)
```

<a name="section-alignmentdataset"></a>

<a name="section-alignmentdataset-2"></a>

## AlignmentDataset

[source](source.md#section-alignmentdataset)

```python
AlignmentDataset (returned by Dataset.load or construct)
```

The existing immutable dataset record holds graph topology and the separate reference used for construction or post-inference analysis.

| Field / method | Meaning |
| --- | --- |
| root / name | Resolved instance directory and dataset name. |
| graph1 / graph2 | Source and target NetworkX graphs in local index space. |
| ground\_truth | Local-ID source-to-target reference mapping. |
| g1\_old\_to\_new / g1\_new\_to\_old | Source original/local ID maps. |
| g2\_old\_to\_new / g2\_new\_to\_old | Target original/local ID maps. |
| metadata | Loaded provenance and annotation-scope information. |
| source\_only\_nodes / target\_only\_nodes | Reference-complement node sets; not proof of nonmatchability when annotation is incomplete. |
| source\_overlap\_ratio / target\_overlap\_ratio | Reference pair count divided by the corresponding graph order. |
| node\_jaccard\_overlap | Reference pair count divided by the node-identity union size. |
| pairs\_to\_original(pairs) | Convert local-ID predicted pairs to original IDs. |
| pairs\_to\_reindexed(pairs) | Convert original-ID pairs to local IDs; reject unknown IDs. |
| summary() | Graph/reference counts, structural statistics and available construction protocol. |

The record is frozen, but the contained NetworkX graphs and metadata are Python objects. Treat a loaded reference as evaluation information, not as an algorithm input.

<a name="section-alignmentresult"></a>

<a name="section-alignmentresult-2"></a>

## AlignmentResult

[source](source.md#section-alignmentresult)

```python
AlignmentResult(method, predicted_pairs, runtime_sec, ...)
```

The shared result type is exported directly as `bp.AlignmentResult`. Custom adapters return this type; result optional fields depend on the method.

| Field | Type / default | Meaning |
| --- | --- | --- |
| method | str; required | Method identifier. |
| predicted\_pairs | list\[tuple\[int, int\]\]; required | Native source/target pairs in local index space. |
| runtime\_sec | float; required | Runtime reported by the adapter. |
| peak\_memory\_mb | float \| None = None | Optional method-reported peak memory. |
| score\_matrix / cost\_matrix | np.ndarray \| None = None | Optional source × target continuous outputs. |
| source\_embeddings / target\_embeddings | np.ndarray \| None = None | Optional row-aligned node embeddings. |
| ranking\_candidates | list\[(source, target, score)\] \| None = None | Sparse native retrieved candidates; omitted pairs are not retrieved. |
| larger\_is\_better | bool \| None = None | Score direction; False negates score\_matrix for evaluation. |
| partial\_decoder\_data | dict\[str, np.ndarray\] \| None = None | Optional ephemeral method-native decoder signals. |
| metadata | dict; default empty | Method-specific provenance and diagnostics. |
| stage\_score\_matrices | dict; default empty | Optional source × target method-stage matrices. |
| stage\_diagnostics\_metadata | dict; default empty | Metadata associated with optional stages. |

<a name="section-validation"></a>

### Validation

`validate_shapes(n_source, n_target)` checks matrix/embedding/stage shapes and sparse candidate validity. Public alignment/evaluation additionally check native pair ranges and validated nonfinite outputs. Exact duplicate native pairs and repeated endpoints are reported rather than silently converted into a common one-to-one prediction.

**Python**

```python
result = bp.AlignmentResult(
    method="custom", predicted_pairs=[], runtime_sec=0.0)
```

<a name="section-evaluate"></a>

<a name="section-evaluate-2"></a>

## evaluate

[source](../src/bpupga/_api.py#L261)

```python
evaluate(result, dataset, *, ks=(1, 5, 10)) -> dict
```

Evaluate native pairs and available same-fit rankings. No new decoder or alignment fit is run.

<a name="section-parameters-5"></a>

### Parameters

| Name | Type / default | Description |
| --- | --- | --- |
| result | AlignmentResult; required | Result using the dataset's local index space. |
| dataset | AlignmentDataset; required | Graph orders and the separate reference mapping. |
| ks | Sequence\[int\] = (1, 5, 10) | Nonempty positive integer ranking cutoffs; booleans are rejected. |

<a name="section-returns-4"></a>

### Returns

A dictionary containing `pair`, `matchability`, `overlap_estimation`, `node_classification`, `validity`, `runtime`, `reference_note`, `ranking` and `ranking_policy`, plus method/availability-dependent fields.

<a name="section-raises-5"></a>

### Raises

`ValueError` for invalid cutoffs or incompatible output indices/shapes; `TypeError` for an incompatible result type; `FloatingPointError` for guarded/nonfinite validated results. Metric-module dependency errors propagate.

**Python**

```python
metrics = bp.evaluate(result, data, ks=(1, 5, 10))
print(metrics["pair"]["f1"])
```

See [the complete report-key guide](evaluation.md#section-report-fields).

<a name="section-diagnose"></a>

<a name="section-diagnose-2"></a>

## diagnose

[source](../src/bpupga/_api.py#L349)

```python
diagnose(result, dataset, *, ks=(1, 5, 10), example_limit=10, max_dense_entries=25_000_000) -> dict
```

Run the existing post-inference diagnostics without saving files or rerunning the method. Full diagnostics need the sibling legacy evaluation source.

<a name="section-parameters-6"></a>

### Parameters

| Name | Type / default | Description |
| --- | --- | --- |
| result / dataset | AlignmentResult / AlignmentDataset | Completed local-ID result and separate reference-bearing dataset. |
| ks | Sequence\[int\] = (1, 5, 10) | Positive ranking cutoffs. |
| example\_limit | int = 10 | Maximum traceable examples in each applicable category; nonnegative. |
| max\_dense\_entries | int = 25\_000\_000 | Entry limit for dense diagnostic representations; positive. |

<a name="section-returns-5"></a>

### Returns

A diagnostic report with native-output accounting, score-space availability, directional analyses and applicable signal/decoder comparisons. Incomplete references return explicit skipped-diagnostic reasons.

<a name="section-raises-6"></a>

### Raises

`ValueError` for invalid cutoffs, limits or result shape/index constraints; `FileNotFoundError` if required legacy source is missing; validation and dependency errors propagate.

Reference-derived oracle endpoint masks are post-hoc and labeled. The separate true-cardinality oracle remains disabled by this wrapper.

**Python**

```python
report = bp.diagnose(result, data, max_dense_entries=5_000_000)
print(report["score_space"])
```

See [diagnostic interpretation and scope](diagnostics.md).

<a name="section-runlog-open"></a>

<a name="section-runlog-open-2"></a>

## RunLog.open

[source](../src/bpupga/_api.py#L408)

```python
RunLog.open(attempt_dir: str | Path) -> RunLog
```

Read an existing campaign attempt snapshot. It uses `result.json` when present, otherwise `started.json`, and reads an optional `fit_failure.json`.

<a name="section-parameters-7"></a>

### Parameters

`attempt_dir`: existing attempt directory. No matrices are loaded and no campaign files are changed.

<a name="section-returns-6"></a>

### Returns

A `RunLog` record with the properties below. Reopen the directory to refresh its snapshot.

<a name="section-raises-7"></a>

### Raises

`FileNotFoundError` for absent record files; `ValueError` for a non-object record or missing string status. JSON decoding and file access errors propagate.

**Python**

```python
run = bp.RunLog.open(attempt_dir)
print(run.status)
print(run.native_metrics)
```

<a name="section-runlog-properties"></a>

<a name="section-runlog-properties-and-summary"></a>

## RunLog properties and summary

[source](../src/bpupga/_api.py#L396)

```python
run.status; run.native_metrics; run.runtime; run.errors; run.summary()
```

| Property / method | Result |
| --- | --- |
| status | Recorded status string. |
| native\_metrics | Deep copy of variants.native for SUCCESS; None for other statuses or absent metrics. |
| runtime | Existing runtime dictionary, with top-level end\_to\_end\_seconds incorporated if recorded. |
| errors | Recorded top-level error/traceback and optional fit\_failure details. |
| summary() | attempt\_dir, status, task, native\_metrics, runtime, and errors. |

A successful zero score remains a valid number. Timeout, OOM, numerical error, incompatibility and unfinished attempts keep missing native scores rather than receiving artificial zeros. See the [run-log guide and local inspector](logs.md).

<a name="section-register-algorithm"></a>

<a name="section-register-algorithm-2"></a>

## register_algorithm

[source](../src/bpupga/_api.py#L112)

```python
register_algorithm(name: str, factory: Callable[..., Any]) -> None
```

Associate a new method name with a user-provided adapter factory.

<a name="section-factory-contract"></a>

### Factory contract

**Python**

```python
def factory(*, parameters, seed, device, dataset_family):
    return adapter  # adapter.fit(graph1, graph2) -> bp.AlignmentResult

bp.register_algorithm("my_method", factory)
```

The factory receives configuration and execution settings, not a reference-bearing dataset. Custom adapters must maintain the unsupervised contract themselves; the in-process API cannot police arbitrary filesystem reads.

<a name="section-raises-8"></a>

### Raises

`ValueError` for an empty/untrimmed name or an already registered/reserved name; `TypeError` for a noncallable factory. Built-in names and the supervised `opgm` name cannot be replaced.

See [the complete custom adapter example](extending.md).

---

[Repository home](../README.md) · [Documentation index](documentation-index.md) · [← Custom algorithms](extending.md) · [Troubleshooting →](faq.md)
