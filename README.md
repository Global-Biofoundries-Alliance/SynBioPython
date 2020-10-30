# SynBioPython

[![Build Status](https://travis-ci.org/Global-Biofoundries-Alliance/SynBioPython.svg?branch=master)](https://travis-ci.org/Global-Biofoundries-Alliance/SynBioPython)

Synbiopython provides generic tools for Synthetic Biology.


## Installation

```bash
pip install synbiopython
```

To install the latest version from Github:
```
pip install --user git+https://github.com/Global-Biofoundries-Alliance/SynBioPython
```


## Usage

You should now be able to run this in Python:

```python
import synbiopython
print(synbiopython.__version__)
```

Currently, there are three modules implemented:
- The genbabel module provides standard file parsers and for working with multiple fileformats.
- The codon module provides support for codon optimisation.
- The lab automation module enables working with plates and generation of picklists (transfers) for liquid handlers.


### Examples

Example Jupyter notebooks are provided for each module: [codon](https://github.com/Global-Biofoundries-Alliance/SynBioPython/blob/master/examples/codon.ipynb), [genbabel](https://github.com/Global-Biofoundries-Alliance/SynBioPython/blob/master/examples/genbabel.ipynb) and [lab automation](https://github.com/Global-Biofoundries-Alliance/SynBioPython/blob/master/examples/lab_automation.ipynb). In order to open these notebooks, download and install [JupyterLab](https://jupyterlab.readthedocs.io).


## Contribute!

SynBioPython is developed collectively by members of the Global Biofoundry Alliance and released on Github under the MIT license. Contributions are welcome!
