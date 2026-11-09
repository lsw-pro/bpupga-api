[Repository home](../README.md) · [Documentation index](documentation-index.md) · [← Quick start](quickstart.md) · [Algorithms →](algorithms.md)

# Datasets and construction

Load prepared graph pairs, preserve their node membership, and construct controlled bilateral partial overlap.

<a name="section-file-format"></a>

## The common file format

A prepared instance is a directory with integer edge lists and an injective reference mapping. Explicit node files are how isolated nodes enter the graphs.

| File | Requirement | Meaning |
| --- | --- | --- |
| G1.edgelist | Required | Source graph: at least two integer IDs per non-comment edge line |
| G2.edgelist | Required | Target graph in the same format |
| Alignment.json | Required | JSON mapping original source IDs to original target IDs, e.g. {"10": 20} |
| G1.nodes / G2.nodes | Optional | One integer ID per line; include isolates here |
| metadata.json | Optional | JSON object containing provenance and reference limitations |

The loader builds simple undirected graphs, removes self-loops, sorts original integer IDs, and assigns contiguous local IDs. Original IDs need not match across the two graphs. The reference must be one-to-one and its endpoints must exist.

<a name="section-load"></a>

## Load and inspect an instance

**Load a graph pair**

```python
import bpupga as bp

data = bp.Dataset.load("data/my_pair")
print(data.summary())
print(data.graph1.number_of_nodes())
print(data.graph2.number_of_nodes())
print(data.g1_new_to_old)
```

The loaded [AlignmentDataset](api.md#section-alignmentdataset) retains both graphs, the reference, metadata, and ID maps. Pass `data.graph1` and `data.graph2` to an algorithm; keep the dataset object for evaluation.

<a name="section-node-identifiers"></a>

## Convert prediction identifiers

**ID conversion**

```python
original_pairs = data.pairs_to_original(result.predicted_pairs)
local_pairs = data.pairs_to_reindexed(original_pairs)
```

<a name="section-partial-overlap"></a>

## Construct bilateral partial overlap

The existing constructor partitions matched identities into shared, source-only, and target-only groups. It keeps the induced edges of retained nodes and excludes preexisting unmatched identities from this controlled pool. The source and target ratios can be set separately.

**Construct an instance**

```python
base = bp.Dataset.load("data/base_pair")
partial = bp.construct(
    base.root,
    rho_source=0.8,
    rho_target=0.6,
    construction_seed=2026,
    output_dir="runs/partial_2026")
print(partial.summary())
```

`output_dir` must be new. Construction does not overwrite an existing directory. The source files are read-only inputs. Requested ratios are node overlap, not edge-deletion rates; finite graph sizes produce integer allocation and realized overlap recorded in metadata. The constructor keeps original IDs; loading performs sorted local reindexing.

<a name="section-natural-pairs"></a>

## Natural pairs and incomplete annotations

Load natural graph pairs directly to preserve their observed populations and overlap. Reconstructing them through the controlled pool changes the task. If a reference is incomplete, unannotated nodes cannot be treated as confirmed unmatched nodes.

**metadata.json**

```json
{
  "ground_truth_complete": false,
  "groundtruth_limitations": "Only verified correspondences are annotated."
}
```

The facade detects `groundtruth_limitations` or a false completeness flag and skips label-dependent matchability, overlap, and private-node diagnostics. Pair and ranking scores remain relative to the supplied reference.

<a name="section-custom-dataset"></a>

## Use your own dataset

Export your data using the same filenames and mapping format, then call `Dataset.load`. A special dataset subclass is unnecessary. See [toy\_example.py](../examples/toy_example.py) for a complete six-file example created with ordinary Python file operations, and the [loader reference](api.md#section-dataset-load) for errors and returned fields.

---

[Repository home](../README.md) · [Documentation index](documentation-index.md) · [← Quick start](quickstart.md) · [Algorithms →](algorithms.md)
