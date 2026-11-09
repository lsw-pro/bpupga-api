# Documentation index

Use your browser's **Find** (Ctrl+F / Command+F) to locate a topic, then follow its section link. All links remain within this repository.

[Repository home](../README.md)

| Topic | Page |
| --- | --- |
| [BPUPGA documentation](index.md) | A Python interface for bilateral partial graph alignment: prepare graph pairs, configure methods, align, evaluate, and inspect results. |
| [Start here](index.md#section-start-here) | BPUPGA documentation |
| [Install & import](index.md#section-install-import) | BPUPGA documentation |
| [A complete example](index.md#section-a-complete-example) | BPUPGA documentation |
| [Find an interface](index.md#section-find-an-interface) | BPUPGA documentation |
| [The alignment workflow](index.md#section-workflow) | BPUPGA documentation |
| [Documentation map](index.md#section-documentation-map) | BPUPGA documentation |
| [Scope](index.md#section-scope) | BPUPGA documentation |
| [Installation](installation.md) | Use the existing model environment and import the API from the consolidated api directory. |
| [Requirements](installation.md#section-requirements) | Installation |
| [Option A · set PYTHONPATH](installation.md#section-pythonpath) | Installation |
| [Option B · editable checkout install](installation.md#section-editable-install) | Installation |
| [Local layout](installation.md#section-layout) | Installation |
| [Check the setup](installation.md#section-check-setup) | Installation |
| [Quick start](quickstart.md) | A complete first example, followed by a configurable example for prepared benchmark data. |
| [1. Run a self-contained toy example](quickstart.md#section-toy-example) | Quick start |
| [2. Align a prepared benchmark instance](quickstart.md#section-prepared-example) | Quick start |
| [3. Read the result](quickstart.md#section-read-result) | Quick start |
| [Next steps](quickstart.md#section-next-steps) | Quick start |
| [Datasets and construction](datasets.md) | Load prepared graph pairs, preserve their node membership, and construct controlled bilateral partial overlap. |
| [The common file format](datasets.md#section-file-format) | Datasets and construction |
| [Load and inspect an instance](datasets.md#section-load) | Datasets and construction |
| [Convert prediction identifiers](datasets.md#section-node-identifiers) | Datasets and construction |
| [Construct bilateral partial overlap](datasets.md#section-partial-overlap) | Datasets and construction |
| [Natural pairs and incomplete annotations](datasets.md#section-natural-pairs) | Datasets and construction |
| [Use your own dataset](datasets.md#section-custom-dataset) | Datasets and construction |
| [Algorithms](algorithms.md) | Choose a current adapter, configure real method parameters, and use a shared alignment call. |
| [Choose a method](algorithms.md#section-choose-a-method) | Algorithms |
| [Configure a method](algorithms.md#section-configure-a-method) | Algorithms |
| [Execution settings and dependencies](algorithms.md#section-execution-settings) | Algorithms |
| [Original-author CPU ALPINE](algorithms.md#section-author-alpine) | Algorithms |
| [S-GWL numerical revision](algorithms.md#section-sgwl-numerics) | Algorithms |
| [Custom methods](algorithms.md#section-custom-methods) | Algorithms |
| [Evaluation and metrics](evaluation.md) | Interpret native pair scores, endpoint selection, overlap, ranking provenance and report availability. |
| [Exact-pair recovery](evaluation.md#section-pair-recovery) | Evaluation and metrics |
| [Endpoint matchability and overlap](evaluation.md#section-matchability) | Evaluation and metrics |
| [Node classification](evaluation.md#section-node-classification) | Evaluation and metrics |
| [Directional ranking](evaluation.md#section-ranking) | Evaluation and metrics |
| [Returned report](evaluation.md#section-report-fields) | Evaluation and metrics |
| [Incomplete reference annotations](evaluation.md#section-incomplete-reference) | Evaluation and metrics |
| [Campaign decoder views](evaluation.md#section-campaign-decoder-views) | Evaluation and metrics |
| [Report repeated runs](evaluation.md#section-reporting-seeds) | Evaluation and metrics |
| [Post-inference diagnostics](diagnostics.md) | Analyze native errors and score-level signals with explicit reference scope and oracle labeling. |
| [Available analyses](diagnostics.md#section-available-analyses) | Post-inference diagnostics |
| [Oracle comparisons are analysis-only](diagnostics.md#section-oracle-scope) | Post-inference diagnostics |
| [Missing data and matrix limits](diagnostics.md#section-skip-reasons) | Post-inference diagnostics |
| [Incomplete labels](diagnostics.md#section-incomplete-diagnostic-labels) | Post-inference diagnostics |
| [Source-checkout dependency](diagnostics.md#section-diagnostic-dependency) | Post-inference diagnostics |
| [Saved runs and resources](logs.md) | Read a campaign attempt and inspect its existing status, native metrics, resource records, and errors. |
| [Read an existing attempt](logs.md#section-read-an-attempt) | Saved runs and resources |
| [Status and native scores](logs.md#section-status-and-scores) | Saved runs and resources |
| [Timing and memory scope](logs.md#section-resources) | Saved runs and resources |
| [Inspect a local run record](logs.md#section-inspector) | Saved runs and resources |
| [Read logs from a script](logs.md#section-offline-script) | Saved runs and resources |
| [Custom algorithms](extending.md) | Register a graph-only adapter and reuse the shared result and evaluation contracts. |
| [The adapter contract](extending.md#section-adapter-contract) | Custom algorithms |
| [A minimal custom adapter](extending.md#section-complete-adapter) | Custom algorithms |
| [Return optional score data](extending.md#section-optional-outputs) | Custom algorithms |
| [Registration and reproducibility](extending.md#section-registration) | Custom algorithms |
| [Python API reference](api.md) | Signatures, parameters, return fields, exceptions and examples for the exported BPUPGA interface. |
| [Dataset.load](api.md#section-dataset-load-2) | Python API reference |
| [Parameters](api.md#section-parameters) | Python API reference |
| [Returns](api.md#section-returns) | Python API reference |
| [Raises](api.md#section-raises) | Python API reference |
| [construct](api.md#section-construct-2) | Python API reference |
| [Parameters](api.md#section-parameters-2) | Python API reference |
| [Returns](api.md#section-returns-2) | Python API reference |
| [Notes](api.md#section-notes) | Python API reference |
| [Raises](api.md#section-raises-2) | Python API reference |
| [Algorithm](api.md#section-algorithm-2) | Python API reference |
| [Parameters](api.md#section-parameters-3) | Python API reference |
| [Attributes](api.md#section-attributes) | Python API reference |
| [Raises](api.md#section-raises-3) | Python API reference |
| [Algorithm.align](api.md#section-algorithm-align-2) | Python API reference |
| [Parameters](api.md#section-parameters-4) | Python API reference |
| [Returns](api.md#section-returns-3) | Python API reference |
| [Raises](api.md#section-raises-4) | Python API reference |
| [Notes](api.md#section-notes-2) | Python API reference |
| [AlignmentDataset](api.md#section-alignmentdataset-2) | Python API reference |
| [AlignmentResult](api.md#section-alignmentresult-2) | Python API reference |
| [Validation](api.md#section-validation) | Python API reference |
| [evaluate](api.md#section-evaluate-2) | Python API reference |
| [Parameters](api.md#section-parameters-5) | Python API reference |
| [Returns](api.md#section-returns-4) | Python API reference |
| [Raises](api.md#section-raises-5) | Python API reference |
| [diagnose](api.md#section-diagnose-2) | Python API reference |
| [Parameters](api.md#section-parameters-6) | Python API reference |
| [Returns](api.md#section-returns-5) | Python API reference |
| [Raises](api.md#section-raises-6) | Python API reference |
| [RunLog.open](api.md#section-runlog-open-2) | Python API reference |
| [Parameters](api.md#section-parameters-7) | Python API reference |
| [Returns](api.md#section-returns-6) | Python API reference |
| [Raises](api.md#section-raises-7) | Python API reference |
| [RunLog properties and summary](api.md#section-runlog-properties-and-summary) | Python API reference |
| [register_algorithm](api.md#section-register-algorithm-2) | Python API reference |
| [Factory contract](api.md#section-factory-contract) | Python API reference |
| [Raises](api.md#section-raises-8) | Python API reference |
| [Troubleshooting and FAQ](faq.md) | Resolve import, dependency, graph-format, annotation-scope and saved-run questions. |
| [Python cannot import bpupga](faq.md#section-import) | Troubleshooting and FAQ |
| [“common is already loaded from another checkout”](faq.md#section-checkout-collision) | Troubleshooting and FAQ |
| [Missing PyTorch, scikit-learn, vendor packages, or weights](faq.md#section-dependencies) | Troubleshooting and FAQ |
| [Does device='cpu' mean every implementation is lightweight?](faq.md#section-devices) | Troubleshooting and FAQ |
| [Why does align reject my graph?](faq.md#section-graph-input) | Troubleshooting and FAQ |
| [Why does construct refuse the output directory?](faq.md#section-output-dir) | Troubleshooting and FAQ |
| [Requested and realized overlap differ slightly](faq.md#section-ratios) | Troubleshooting and FAQ |
| [What if my correspondences are incomplete?](faq.md#section-reference-completeness) | Troubleshooting and FAQ |
| [Why is ranking None?](faq.md#section-missing-ranking) | Troubleshooting and FAQ |
| [Why is Pair F1 present when is_one_to_one is false?](faq.md#section-noninjective) | Troubleshooting and FAQ |
| [Diagnostics cannot find diagnostics.py](faq.md#section-diagnose-missing) | Troubleshooting and FAQ |
| [RunLog has no native_metrics](faq.md#section-log-result) | Troubleshooting and FAQ |
| [Where are train, checkpoint, resume, and plot_curve?](faq.md#section-training) | Troubleshooting and FAQ |
| [Will default API calls reproduce the paper tables?](faq.md#section-reproduce) | Troubleshooting and FAQ |
| [Source code](source.md) | The public facade implementation used to build this documentation. Line links identify the actual implementation of each interface. |
| [AlignmentDataset](source.md#section-alignmentdataset) | Source code |
| [AlignmentResult](source.md#section-alignmentresult) | Source code |
