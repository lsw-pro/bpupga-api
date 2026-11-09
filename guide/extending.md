[Repository home](../README.md) · [Documentation index](documentation-index.md) · [← Saved runs & resources](logs.md) · [Python API reference →](api.md)

# Custom algorithms

Register a graph-only adapter and reuse the shared result and evaluation contracts.

<a name="section-adapter-contract"></a>

## The adapter contract

A registered factory receives `parameters`, `seed`, `device`, and `dataset_family` as keyword arguments. It returns an object implementing `fit(graph1, graph2)`, which returns `bp.AlignmentResult`.

The public `Algorithm.align` method passes copies of simple, loop-free graph topology with graph, node, and edge attributes removed. It accepts contiguous local IDs, as produced by `Dataset.load`.

<a name="section-complete-adapter"></a>

## A minimal custom adapter

**Custom adapter**

```python
import bpupga as bp

class DegreeAdapter:
    def fit(self, graph1, graph2):
        source = sorted(graph1, key=lambda u: (-graph1.degree(u), u))
        target = sorted(graph2, key=lambda v: (-graph2.degree(v), v))
        return bp.AlignmentResult(
            method="degree_example",
            predicted_pairs=list(zip(source, target)),
            runtime_sec=0.0)

def factory(*, parameters, seed, device, dataset_family):
    return DegreeAdapter()

bp.register_algorithm("degree_example", factory)
method = bp.Algorithm("degree_example", seed=2026)
# data is an AlignmentDataset loaded with Dataset.load.
result = method.align(data.graph1, data.graph2)
report = bp.evaluate(result, data)
```

This degree matcher demonstrates the interface; its runtime field is illustrative. Your adapter should measure its own computation and honor the supplied execution settings. A self-contained version including the input data is available as [toy\_example.py](../examples/toy_example.py).

<a name="section-optional-outputs"></a>

## Return optional score data

Return a score matrix or cost matrix with shape `(len(graph1), len(graph2))` to enable ranking evaluation. For scores, set `larger_is_better` to identify their direction. Paired embeddings and sparse scored candidates are supported by the result contract; missing sparse candidates are not invented.

**Optional continuous output**

```python
result = bp.AlignmentResult(
    method="my_method",
    predicted_pairs=pairs,
    runtime_sec=elapsed_seconds,
    score_matrix=scores,
    larger_is_better=True,
    metadata={"score_definition": "my native similarity"})
```

Use native predictions as returned by your method. The evaluator records repeated endpoints; it does not silently force them into a matching. Out-of-range predictions and non-finite returned arrays are rejected.

<a name="section-registration"></a>

## Registration and reproducibility

Names cannot replace a built-in or an existing registration. Use a new name for a changed adapter. The factory does not receive the reference-bearing dataset; custom code remains responsible for obeying the unsupervised information contract. Local registration is distinct from adding a method to a frozen benchmark campaign.

See [register\_algorithm](api.md#section-register-algorithm) and [AlignmentResult](api.md#section-alignmentresult) for exact arguments and fields.

---

[Repository home](../README.md) · [Documentation index](documentation-index.md) · [← Saved runs & resources](logs.md) · [Python API reference →](api.md)
