# BPUPGA API

Unsupervised bilateral partial graph alignment: Python API documentation, tutorials, source snapshots, and runnable examples.

全部文档均可直接在本 GitHub 仓库阅读，无需跳转到独立网站。

**Start here:** [Installation](guide/installation.md) · [Quick start](guide/quickstart.md) · [Python API](guide/api.md) · [Source code](guide/source.md) · [Examples](examples/README.md)

## Documentation

| Guide | Contents |
| --- | --- |
| [Overview](guide/index.md) | Scope, workflow, and documentation map |
| [Installation](guide/installation.md) | Environment, imports, and local installation |
| [Quick start](guide/quickstart.md) | Toy example and prepared benchmark examples |
| [Datasets & construction](guide/datasets.md) | Graph files, identifiers, partial overlap, and natural pairs |
| [Algorithms](guide/algorithms.md) | Twelve methods, parameters, execution settings, and custom adapters |
| [Evaluation](guide/evaluation.md) | Pair recovery, node matchability, ranking, and incomplete references |
| [Diagnostics](guide/diagnostics.md) | Error decomposition and reference-assisted diagnostics |
| [Saved runs & resources](guide/logs.md) | Saved metrics, status, resources, and local JSON inspection |
| [Custom algorithms](guide/extending.md) | Register a graph-only adapter and optional outputs |
| [Python API reference](guide/api.md) | Signatures, parameters, defaults, returns, exceptions, and source lines |
| [Troubleshooting](guide/faq.md) | Imports, dependencies, devices, outputs, and metric errors |
| [Source code](guide/source.md) | Facade implementation and shared result/data records |

## Find a topic

Open the [complete documentation index](guide/documentation-index.md) and use **Ctrl+F / Command+F**. GitHub's **Outline** menu also lists the sections on each documentation page.

## Examples and source

- [Self-contained toy example](examples/toy_example.py)
- [All 48 prepared method/dataset combinations](examples/README.md)
- [Download the examples](examples/examples.zip)
- [Facade source with native line numbers](src/bpupga/_api.py)
- [Shared dataset record](src/records/AlignmentDataset.py) and [alignment result](src/records/AlignmentResult.py)

## Execution requirements

This repository contains documentation, source snapshots, and examples. Running the built-in models requires the complete BPUPGA research checkout, existing data, and method dependencies described in [Installation](guide/installation.md). This repository alone is not a standalone release of all models or datasets.

The toy example illustrates the API with temporary data and a custom adapter; it is not a benchmark result. Reference information is used for evaluation and explicitly labeled diagnostics, not passed to unsupervised fitting.
