[Repository home](../README.md) · [Documentation index](documentation-index.md) · [Installation →](installation.md)

# BPUPGA documentation

A Python interface for bilateral partial graph alignment: prepare graph pairs, configure methods, align, evaluate, and inspect results.

> **Version 0.1 · local research checkout** The library runs in your Python environment. These documents describe its use and provide a local run-record inspector.

<a name="section-start-here"></a>

## Start here

01 / SETUP

<a name="section-install-import"></a>

### Install & import

Use the project environment and add the API to your Python path.

[Read this guide](installation.md)

02 / FIRST RUN

<a name="section-a-complete-example"></a>

### A complete example

Try a temporary toy graph pair or a prepared benchmark instance.

[Read this guide](quickstart.md)

03 / REFERENCE

<a name="section-find-an-interface"></a>

### Find an interface

Signatures, parameters, returns, exceptions, and source code.

[Read this guide](api.md)

<a name="section-workflow"></a>

## The alignment workflow

`Dataset / construct` → `Algorithm.align` → `evaluate / diagnose`

Data loading retains graph topology, reference correspondences, and identifier maps. Algorithms receive graph topology. Evaluation and diagnostics use the reference after inference. `RunLog` provides a separate read-only view of recorded campaign attempts.

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

<a name="section-documentation-map"></a>

## Documentation map

| Topic | What you will find |
| --- | --- |
| Data preparation | File schema, isolated nodes, ID maps, and bilateral-overlap construction |
| Algorithms | The twelve current method identifiers, configuration, and dependencies |
| Evaluation | Native pair recovery, node matchability, overlap, validity, and available rankings |
| Diagnostics | Post-inference error analysis, score signals, and oracle interpretation |
| Saved runs | Status, native metrics, timing, memory, errors, and the local JSON inspector |
| Extending | A custom graph-only adapter using the shared AlignmentResult contract |

<a name="section-scope"></a>

## Scope

The convenience API reuses the implementations and data tools in this repository. Formal campaign scheduling, device allocation, resource limits, and result sealing remain with the campaign runner. Adapter defaults do not automatically reproduce a frozen campaign profile.

Use [Troubleshooting](faq.md) for dependency, import, and unavailable-output questions.

---

[Repository home](../README.md) · [Documentation index](documentation-index.md) · [Installation →](installation.md)
