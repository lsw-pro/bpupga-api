[Repository home](../README.md) · [Documentation index](documentation-index.md) · [← Installation](installation.md) · [Datasets & construction →](datasets.md)

# Quick start

A complete first example, followed by a configurable example for prepared benchmark data.

<a name="section-toy-example"></a>

## 1. Run a self-contained toy example

The example creates a tiny graph pair in a temporary directory, registers a degree-based adapter, and calls the same load → align → evaluate workflow. The adapter demonstrates the interface and makes no research performance claim.

[↓ Download toy\_example.py](../examples/toy_example.py) [↓ All examples](../examples/examples.zip)

**toy_example.py**

```python
"""Run a small local API example without invoking a built-in model.

From the repository root, set PYTHONPATH=baseline_exdit_261029/api.
This degree-based adapter illustrates the contract; it is not a baseline claim.
"""
import json
import tempfile
from pathlib import Path

import bpupga as bp


class DegreeAdapter:
    def fit(self, graph1, graph2):
        source = sorted(graph1, key=lambda u: (-graph1.degree(u), u))
        target = sorted(graph2, key=lambda v: (-graph2.degree(v), v))
        return bp.AlignmentResult(
            method="degree_example",
            predicted_pairs=list(zip(source, target)),
            runtime_sec=0.0,
        )


def factory(*, parameters, seed, device, dataset_family):
    return DegreeAdapter()


def main():
    bp.register_algorithm("degree_example", factory)
    with tempfile.TemporaryDirectory(prefix="bpupga-demo-") as directory:
        root = Path(directory)
        (root / "G1.edgelist").write_text("10 11\n11 12\n")
        (root / "G2.edgelist").write_text("20 21\n21 22\n")
        (root / "G1.nodes").write_text("10\n11\n12\n13\n")
        (root / "G2.nodes").write_text("20\n21\n22\n23\n")
        (root / "Alignment.json").write_text(
            json.dumps({"10": 20, "11": 21, "12": 22}))
        (root / "metadata.json").write_text(json.dumps({
            "purpose": "API toy example",
            "ground_truth_complete": True,
        }))
        data = bp.Dataset.load(root)
        method = bp.Algorithm("degree_example", seed=2026)
        result = method.align(data.graph1, data.graph2)
        report = bp.evaluate(result, data)
        print("Pair metrics:", report["pair"])
        print("Validity:", report["validity"])
        print("Original IDs:", data.pairs_to_original(result.predicted_pairs))
        print("Ranking availability:", report["ranking_policy"])


if __name__ == "__main__":
    main()
```

<a name="section-prepared-example"></a>

## 2. Align a prepared benchmark instance

Run from the repository root with the import setup in [Installation](installation.md). Choose a method and dataset from the [complete example directory](../examples/README.md); each combination is a separate Python file. Available dependencies and supported devices follow the selected implementation; the example defaults to CPU.

**quickstart.py**

```python
import bpupga as bp

data = bp.Dataset.load(
    "baseline_exdit_261029/date_261023/fbtw/bpupga/"
    "rho_s0p6_rho_t0p6/construction_seed_2026")
method = bp.Algorithm(
    "grampa", parameters={"eta": 1.0}, seed=2026, device="cpu")
result = method.align(data.graph1, data.graph2)
metrics = bp.evaluate(result, data, ks=(1, 5, 10))
print(metrics["pair"])
```

These choices produce example calls. They do not load a campaign's frozen parameter overrides or initiate remote computation. See the [method catalog](algorithms.md) before running a more expensive method.

<a name="section-read-result"></a>

## 3. Read the result

**Inspect outputs**

```python
print(result.method)
print(result.predicted_pairs[:5])
print(data.pairs_to_original(result.predicted_pairs[:5]))
print(metrics["pair"])
print(metrics["validity"])
print(metrics["ranking_policy"])
```

Native pairs use local integer IDs. Pair metrics deduplicate exact pair repetitions and disclose endpoint conflicts. Rankings are available only when the method returns a suitable score representation. [Evaluation](evaluation.md) explains each report field.

<a name="section-next-steps"></a>

## Next steps

- [Build your own input or a partial-overlap instance.](datasets.md)
- [Inspect errors after alignment.](diagnostics.md)
- [Read an existing campaign attempt without fitting again.](logs.md)
- [Register your own graph-only adapter.](extending.md)

## All prepared example combinations

The 48 method/dataset combinations are listed in [Examples](../examples/README.md). Each link opens a Python file on GitHub.

---

[Repository home](../README.md) · [Documentation index](documentation-index.md) · [← Installation](installation.md) · [Datasets & construction →](datasets.md)
