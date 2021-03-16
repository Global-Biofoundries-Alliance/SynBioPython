# SynBioPython

[![Build Status](https://travis-ci.org/Global-Biofoundries-Alliance/SynBioPython.svg?branch=master)](https://travis-ci.org/Global-Biofoundries-Alliance/SynBioPython)
![](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Global-Biofoundries-Alliance/SynBioPython/master?urlpath=git-pull%3Frepo%3Dhttps%253A%252F%252Fgithub.com%252FGlobal-Biofoundries-Alliance%252FSynBioPython%252Ftree%252Fmaster%252Fexamples%26urlpath%3Dtree%252Fexamples%252Findex.ipynb%26branch%3Dmaster)


SynBiopython provides generic tools for Synthetic Biology. For more details, please see the publication:

SynBiopython: an open-source software library for Synthetic Biology, *Jing Wui Yeoh, Neil Swainston, Peter Vegh, Valentin Zulkower, Pablo Carbonell, Maciej B Holowko, Gopal Peddinti, Chueh Loo Poh.* [Synthetic Biology](https://doi.org/10.1093/synbio/ysab001) (2021) ysab001


## Installation

```bash
pip install synbiopython
```

To install the latest version from Github:
```
pip install git+https://github.com/Global-Biofoundries-Alliance/SynBioPython
```
Currently Python 3.6, 3.7 and 3.8 are supported.


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

SynBiopython is developed collectively by members of the Global Biofoundry Alliance and released on Github under the MIT license. Contributions are welcome!
