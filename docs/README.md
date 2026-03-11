# Documentation: python-rayhunter

This directory contains the [Sphinx](https://www.sphinx-doc.org/) documentation source for `python-rayhunter`.

## Prerequisites

Install the dev dependencies from the project root:

```bash
pip install -r requirements-dev.txt
```

You will also need the package itself installed so autodoc can import it:

```bash
pip install -e .
```

## Building the documentation

### HTML (recommended)

```bash
cd docs
make html
```

The output will be written to `docs/_build/html/`. Open `docs/_build/html/index.html` in a browser to view it.

### Other formats

Sphinx supports several output formats. Run `make help` to see all available builders:

```bash
cd docs
make help
```

Common alternatives:

| Command | Output |
|---|---|
| `make html` | HTML website |
| `make singlehtml` | Single-page HTML |
| `make text` | Plain text |
| `make man` | Unix man pages |
| `make epub` | EPUB e-book |

### Windows

Use `make.bat` instead of `make`:

```bat
cd docs
make.bat html
```

## Cleaning the build

To remove all generated output:

```bash
cd docs
make clean
```
