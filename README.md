# PyUCRio

[![Github tests](https://github.com/ucalgary-srs/pyUCRio/actions/workflows/tests_default.yml/badge.svg)](https://github.com/ucalgary-srs/pyUCRio/actions/workflows/tests_default.yml)
[![PyPI version](https://img.shields.io/pypi/v/pyucrio.svg)](https://pypi.python.org/pypi/pyucrio/)
![PyPI Python versions](https://img.shields.io/pypi/pyversions/pyucrio)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14239005.svg)](https://doi.org/10.5281/zenodo.14239005)

PyUCRio is a Python library providing data access and analysis support for RF instrument data provided by the University of Calgary. This presently includes the NORSTAR riometers, and the SWAN Hyper Spectral Riometers (HSR).

PyUCRio officially supports Python 3.9+.

Some links to help:
- [Example Gallery](https://data.phys.ucalgary.ca/working_with_data/index.html#python)
- [PyUCRio API Reference](https://docs-pyucrio.phys.ucalgary.ca)
- [UCalgary SRS Open Data Platform](https://data.phys.ucalgary.ca)
- [Additional examples](https://github.com/ucalgary-srs/pyUCRio/tree/main/examples)

## Installation

Installation can be done using pip:

```console
$ pip install pyucrio
```

For the most bleeding edge version of PyUCRio, you can install it directly from the Github repository:

```console
$ pip install pyucrio@git+https://github.com/ucalgary-srs/pyUCRio

[OR]

$ git clone https://github.com/ucalgary-srs/pyUCRio.git
$ cd pyUCRio
$ pip install .
```

## Usage

Below is how the library can be imported and initialized:

```python
import pyucrio
rio = pyucrio.PyUCRio()
```

## Contributing

Bug reports, feature suggestions, and other contributions are greatly appreciated!

Templates for bug report and feature suggestions can be found when creating a Github Issue. If you have questions or issues installing PyUCRio, we encourage that you open up a topic in the Github Discussions page.

A large collection of examples can be found in the [`examples`](https://github.com/ucalgary-srs/pyUCRio/tree/main/examples) directory. 
