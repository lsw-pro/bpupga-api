[Repository home](../README.md) · [Documentation index](documentation-index.md) · [← Overview](index.md) · [Quick start →](quickstart.md)

# Installation

Use the existing model environment and import the API from the consolidated api directory.

<a name="section-requirements"></a>

## Requirements

Use Python 3.10 or later. The facade needs NetworkX and NumPy; evaluation uses scikit-learn, and the optional diagnostic implementation uses SciPy. Built-in methods need their existing author dependencies and, where applicable, weights and a supported PyTorch installation.

The complete research checkout is required: the API delegates to sibling implementations in `baseline_exdit_261029/baseline/`, constructors in `date_261023/`, and the existing evaluation code. Diagnostics additionally use `BPUPGA/baseline261023/evaluation/`.

<a name="section-pythonpath"></a>

## Option A · set PYTHONPATH

From the **repository root**, run:

**Terminal**

```bash
export PYTHONPATH="$PWD/baseline_exdit_261029/api${PYTHONPATH:+:$PYTHONPATH}"
python -c "import bpupga; print(bpupga.__file__)"
```

Here `python` means your configured project/model interpreter. If you work from `baseline_exdit_261029/`, use `PYTHONPATH=api` instead.

<a name="section-editable-install"></a>

## Option B · editable checkout install

To keep imports available without setting PYTHONPATH each time, install the local facade into your chosen environment. The following command uses existing environment dependencies:

**Terminal**

```bash
python -m pip install --no-deps --no-build-isolation -e baseline_exdit_261029/api
```

This requires setuptools (64 or newer) in that environment. It installs the distribution `bpupga-local`, imported as `bpupga`. Keep the repository in place: this facade is bound to the surrounding research checkout and is not a standalone wheel or a PyPI release. The command does not install the vendor dependencies of each alignment method.

<a name="section-layout"></a>

## Local layout

**Repository**

```python
baseline_exdit_261029/
├── api/
│   ├── README.md
│   ├── pyproject.toml
│   ├── bpupga/       # Python facade and its tests
│   └── site/         # Documentation source and deployed assets
├── baseline/         # All method implementations, including OPGM-U
├── date_261023/      # Existing datasets and constructors
└── evaluation/      # Existing campaign evaluation
```

<a name="section-check-setup"></a>

## Check the setup

First run the [toy example](../examples/toy_example.py), which uses temporary inputs and a small custom adapter. It does not invoke a built-in method or start a campaign:

**Terminal**

```bash
python toy_example.py
```

For a prepared-data example using GRAMPA, continue to [Quick start](quickstart.md). Start a fresh Python process when switching between historical baseline checkouts, which share module names such as `common`.

---

[Repository home](../README.md) · [Documentation index](documentation-index.md) · [← Overview](index.md) · [Quick start →](quickstart.md)
