[Repository home](../README.md) · [Documentation index](documentation-index.md) · [← Diagnostics](diagnostics.md) · [Custom algorithms →](extending.md)

# Saved runs and resources

Read a campaign attempt and inspect its existing status, native metrics, resource records, and errors.

<a name="section-read-an-attempt"></a>

## Read an existing attempt

**Saved run**

```python
import bpupga as bp

run = bp.RunLog.open(
    "baseline_exdit_261029/evaluation/output/.../attempt_0001")
print(run.status)
print(run.native_metrics)
print(run.runtime)
print(run.errors)
summary = run.summary()
```

Use an existing campaign attempt directory. `RunLog.open` reads `result.json` or falls back to `started.json` for an unfinished attempt. Reopen the object for a refreshed snapshot. It does not load saved matrices, fit a method, or update campaign files. A direct `Algorithm.align` call returns an in-memory result and does not automatically create a campaign attempt or log directory.

<a name="section-status-and-scores"></a>

## Status and native scores

| Record status | native\_metrics | Interpretation |
| --- | --- | --- |
| SUCCESS | Native report when present | Inspect pair, validity and ranking scope |
| RUNNING / PENDING | None | No completed native score |
| TIMEOUT / OOM | None | Resource failure, not a zero-score prediction |
| NUMERICAL\_ERROR / ERROR | None | Execution failure retained with its reason |
| PROTOCOL\_INCOMPATIBLE | None | Method did not run under the selected information contract |

Common, Method-aware, and legacy decoder outputs are separate campaign variants. `native_metrics` selects only the native branch. A valid empty prediction can score zero; an unavailable result remains missing.

<a name="section-resources"></a>

## Timing and memory scope

Resource keys depend on the recorded attempt. Fit wall time, evaluator time, end-to-end time, process-tree RSS, and CUDA allocator measurements have different scopes. Retain device and thread settings when comparing them. These records alone do not establish a controlled scalability experiment.

<a name="section-inspector"></a>

## Inspect a local run record

```bash
node examples/inspect_run.js path/to/result.json
```

[Inspector source](../examples/inspect_run.js). The original native-only validation, missing values, and valid zeros are preserved.

Pass a campaign `result.json` or `started.json` to the standalone inspector. The file is parsed locally on your computer and is not uploaded. This tool does not execute graph alignment.

<a name="section-offline-script"></a>

## Read logs from a script

[Download read\_run.py](../examples/read_run.py) to print a summary as JSON:

**Terminal**

```bash
python read_run.py baseline_exdit_261029/evaluation/output/your_dataset/your_method/your_condition/seed_2026/attempt_0001
```

---

[Repository home](../README.md) · [Documentation index](documentation-index.md) · [← Diagnostics](diagnostics.md) · [Custom algorithms →](extending.md)
