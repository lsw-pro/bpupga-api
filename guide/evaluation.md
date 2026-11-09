[Repository home](../README.md) · [Documentation index](documentation-index.md) · [← Algorithms](algorithms.md) · [Diagnostics →](diagnostics.md)

# Evaluation and metrics

Interpret native pair scores, endpoint selection, overlap, ranking provenance and report availability.

`evaluate` scores the native result after alignment. It does not refit a model or apply a new assignment decoder. Keep the returned native pairs, their feasibility checks, and their ranking representation together when reporting results.

**Evaluate the quickstart result**

```python
metrics = bp.evaluate(result, data, ks=(1, 5, 10))
print(metrics["pair"])
print(metrics["validity"])
print(metrics["ranking_policy"])
```

<a name="section-pair-recovery"></a>

## Exact-pair recovery

Let `P` be the set of distinct native predicted pairs, `T` the reference pair set, and `c = |P ∩ T|`. The standard metrics are:

Pair precision = c / |P|<br> Pair recall = c / |T|<br>Pair F1 = 2c / (|P| + |T|)

Zero denominators use zero. Exact duplicate pairs are counted once for pair-set scoring. Repeated source or target endpoints remain visible in `validity`; a pair score does not establish one-to-one feasibility. A valid empty prediction is distinct from a failed execution.

<a name="section-matchability"></a>

## Endpoint matchability and overlap

Matched-node precision, recall, and F1 compare the unique predicted endpoint set on each graph with the endpoints in the reference. They measure selection of participating nodes separately from correct identity pairing.

Overlap estimates distinguish predicted pair count from distinct source and target coverage. For graph orders `M` and `N`, predicted coverages are `|predicted sources| / M` and `|predicted targets| / N`. Pair count and endpoint count may differ when the native output repeats endpoints.

<a name="section-node-classification"></a>

## Node classification

`node_classification` contains source and target confusion counts, node accuracy, balanced accuracy, and unmatched-node precision/recall/F1. These use the same endpoint-count function as the campaign evaluator. Balanced accuracy is `None` when either reference class is absent. Selecting the correct participating nodes does not establish correct identity pairing; inspect pair recovery separately.

<a name="section-ranking"></a>

## Directional ranking

Hits@k is the fraction of reference-covered queries whose correct counterpart appears at rank k or better. MRR is the mean reciprocal rank. Dense scores rank against all opposite-side input nodes, with lower local candidate IDs breaking exact score ties. Both directions and the arithmetic average of their metric values are returned.

Sparse outputs are ranked within the retrieved candidate lists. An absent true counterpart contributes zero to Hits@k and MRR; omitted scores are not fabricated. When only paired embeddings are present, ranking uses Euclidean distance and records that representation in `ranking_policy`.

GRAMPA exposes its current soft-transformed ranking and the corresponding `raw_ranking`. S-GWL's continuous outputs represent recursive block scores. Ranking metrics answer a covered-query question; they do not measure rejection of unmatched nodes.

<a name="section-report-fields"></a>

## Returned report

| Key | Content | Availability |
| --- | --- | --- |
| method / output\_variant | Method identity; output\_variant is 'native' | Always |
| pair | precision, recall, f1, true\_positive, predicted, ground\_truth | Reference-relative pair accounting |
| matchability | source and target precision/recall/F1 | None for a reference flagged incomplete |
| overlap\_estimation | Pair-count errors and directional endpoint coverage errors | None for a reference flagged incomplete |
| node\_classification | Source/target TP, FP, FN, TN, accuracy, balanced accuracy, unmatched precision/recall/F1 | None for an incomplete reference; balanced accuracy also requires both classes |
| validity | Index ranges, raw/unique pair counts, repeated pair/endpoints, is\_one\_to\_one | Always for a validated result |
| ranking | source\_to\_target, target\_to\_source, bidirectional | None when no usable score/candidate/embedding representation exists |
| ranking\_policy | Score representation, tie rule, or skipped\_reason | Always |
| raw\_ranking | GRAMPA ranking before its soft transform | GRAMPA with a continuous matrix |
| runtime | native\_reported\_seconds; optional peak\_memory\_mb | Existing result measurements |
| reference\_note | Interpretation relative to supplied annotation coverage | Always |
| skipped\_metrics | Reasons matchability, overlap estimates and node classification were skipped | Reference flagged incomplete |

<a name="section-incomplete-reference"></a>

## Incomplete reference annotations

Unannotated nodes are not automatically confirmed unmatched nodes. Mark known limitations in `metadata.json` with a nonempty `groundtruth_limitations` value, or set `ground_truth_complete` or `groundtruth_complete` to `false`. The public API then returns `None` for matchability, overlap estimates and node classification, with explicit reasons. Pair and ranking scores remain relative to the known reference.

> **Annotation scope of campaign records.** Existing campaign files may retain classification and coverage quantities computed against reference-complement sets. Such quantities are annotation-relative when the reference is incomplete; they do not establish that an unannotated node is truly unmatched.

<a name="section-campaign-decoder-views"></a>

## Campaign decoder views

The public `evaluate` function scores native output only. The campaign stores additional decoder views as separate offline analyses of the same saved fit; calling `align` or `evaluate` does not select or apply these extra decoders.

| Saved variant | Decision rule | Interpretation |
| --- | --- | --- |
| native | Pairs returned by the registered method adapter | Primary output; endpoint conflicts remain visible |
| common\_decoder | Mutual top 1% candidates per row/column (at least one), unmatched\_cost=0.05; exact optional assignment with private dummies | Shared post-fit partial one-to-one rule; no true matching size is supplied |
| method\_aware\_decoder | Project-defined rules using the method's native scores, pairs or recorded iteration signals | A method-plus-decoder system, not an author's native output or a universally best rule |
| legacy\_common\_decoder | Earlier rectangular heuristic, retained for comparison | Known private-dummy optimality limitation; not the current Common decoder |

The frozen configuration and variant metadata identify the rules used by each record. All variants share ranking metrics from the same continuous fit scores before hard decoding. A change in pair F1 across decoders is not a new ranking result or another model fit; GRAMPA's soft/raw rankings are score views.

<a name="section-reporting-seeds"></a>

## Report repeated runs

Compute metrics per run before taking means. Report sample standard deviation and successful-run count alongside failure statuses. Do not replace missing scores with zero, calculate mean F1 from mean precision/recall, or treat relabelings of a single natural graph pair as independent graph samples.

Reference: [evaluate](api.md#section-evaluate), [AlignmentResult](api.md#section-alignmentresult), and [saved run records](logs.md).

---

[Repository home](../README.md) · [Documentation index](documentation-index.md) · [← Algorithms](algorithms.md) · [Diagnostics →](diagnostics.md)
