[Repository home](../README.md) · [Documentation index](documentation-index.md) · [← Datasets & construction](datasets.md) · [Evaluation →](evaluation.md)

# Algorithms

Choose a current adapter, configure real method parameters, and use a shared alignment call.

Choose a registered name, provide method-specific parameters, then call the same `align(graph1, graph2)` method. The public interface keeps the reference mapping outside the algorithm call.

<a name="section-choose-a-method"></a>

## Choose a method

The names below select the current project adapters. Parameter excerpts come from the current adapters and public wrapper; they are not a complete parameter list or a promise that omitted defaults reproduce the formal campaign settings.

| Name passed to Algorithm | Display name | Verified configuration excerpts |
| --- | --- | --- |
| alpine | ALPINE | mu=1.0; weight=2; CPU float64; fixed 10 × 10 steps |
| cena | CENA | q=0.5; layers=3; embedding\_dim=64; embedding\_epochs=5 |
| fugal | FUGAL | mu=1.0; niter=15; inner\_iterations=10 |
| gradalign\_plus | GradAlign+ | epochs=10; k\_hop=3; hid\_dim=100; gradual\_iterations=10 |
| grampa | GRAMPA | eta=1.0; center\_adjacency=False; dtype='float64' |
| immnc | iMMNC | k\_de=3; k\_nei=3; initial\_anchor\_ratio=0.04; iterations=10 |
| oiteralign | OIterAlign | dp\_min\_degree=6; diffusion\_step=5; nearest\_candidates=50 |
| opgm\_unsupervised | OPGM-U | layers=5; hidden\_dim=64; epochs=100; learning\_rate=0.001 |
| regal | REGAL | max\_layer=2; alpha=0.01; buckets=2.0; landmark\_seed=42 |
| s\_gwl | S-GWL | partition\_levels=3; cluster\_count=2; outer\_iterations=2000 |
| slotalign | SLOTAlign | bases=2; joint\_epoch=100; epoch=1000; feature\_rounds=3 |
| ulot | ULOT | alpha=0.5; rho=1.0; checkpoint='bundled\_sbm\_50000' |

<a name="section-configure-a-method"></a>

## Configure a method

Use the common `seed` and `device` arguments for execution settings. Put algorithm-specific controls in `parameters`. Configuration is constructed lazily when `align` runs; its effective dictionary is then available as `algorithm.config`.

**Configure and align**

```python
import bpupga as bp

algorithm = bp.Algorithm(
    "grampa",
    parameters={"eta": 1.0, "center_adjacency": False},
    seed=2026,
    device="cpu",
)
# data is the prepared instance loaded in the quickstart.
result = algorithm.align(data.graph1, data.graph2)
print(algorithm.config)
```

<a name="section-execution-settings"></a>

## Execution settings and dependencies

- `device="cpu"` is the facade default. A CUDA request is relevant only when supported by the selected implementation and its installed dependencies.
- Built-in execution imports the existing model environment, including PyTorch. Some methods additionally need vendor packages or bundled weights.
- `dataset_family="Oregon-1"` selects the documented FUGAL numerical policy for that family. It does not supply correspondence labels.
- Topology-derived pseudo-anchors or an internal optimization loop do not create a public training lifecycle. The user entry point remains `align`.

<a name="section-author-alpine"></a>

## Original-author CPU ALPINE

`alpine` calls the archived author's `Alpine` and `Alpine_pp_new` functions through `baseline.alpine_author_cpu`. Both `device="cpu"` and `device="auto"` select CPU; an explicit CUDA request is rejected. Computation uses float64.

The model controls are `mu` and `weight`. The author fixes ten outer iterations, ten inner steps, Sinkhorn regularization 1.0, 500 projection iterations, and tolerance `1e-5`. Corresponding parameter keys must retain these values, including `niter=10`; unsupported controls are rejected.

<a name="section-sgwl-numerics"></a>

## S-GWL numerical revision

`s_gwl` uses the retained-log proximal-state and dual-gauge v2 revision. It preserves the unrounded log transport between proximal updates and normalizes the two scaling factors together, without clipping the kernel or changing the objective or iteration budgets. Inspect `result.metadata["numerical_revision"]` and `result.metadata["numerical_revision_diagnostics"]` for provenance. Temporary hooks are restored after success or failure. Run concurrent S-GWL fits in separate Python processes because the adapter uses module-level hooks.

> **OPGM-U is an explicit adaptation.** Use `opgm_unsupervised` for this project's unsupervised implementation. The original supervised `opgm` name is rejected as incompatible with the unsupervised contract. The two names are not aliases. ULOT's fixed `rho` is a model hyperparameter. Do not populate it from the held-out true overlap.

<a name="section-custom-methods"></a>

## Custom methods

A registered factory returns an adapter with `fit(graph1, graph2)` and an `AlignmentResult` output. The shared public caller is still `Algorithm(...).align(...)`. Follow the [custom-algorithm tutorial](extending.md) for a complete example.

Reference: [Algorithm](api.md#section-algorithm), [align](api.md#section-algorithm-align), and [register\_algorithm](api.md#section-register-algorithm).

---

[Repository home](../README.md) · [Documentation index](documentation-index.md) · [← Datasets & construction](datasets.md) · [Evaluation →](evaluation.md)
