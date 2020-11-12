# pylint: disable=C0103,E0401,W0611
"""
Synbiopython (c) Global BioFoundry Alliance 2020

Synbiopython is licensed under the MIT License.

This module is the test file for the class SEDMLOMEXgen to be used for pytest
"""

import os
import re
import pytest
import synbiopython.genbabel as stdgen

path0 = os.path.abspath(os.path.dirname(__file__))
sbmlfile = "gateNOT_d30_LB_state1_.xml"
sbmlpath = os.path.join(path0, "data", sbmlfile)
phrasedml_str = """
      model1 = model "{}"
      sim1 = simulate uniform(0, 720, 1000)
      sim1.algorithm = rk4
      task1 = run sim1 on model1
      model2 = model model1 with state = 0
      task2 = run sim1 on model2
      plot "Fig 1: Pep (NOT gate 30C LB)" task1.time vs task1.Pep2, task2.Pep2
    """

omexgen = stdgen.SEDMLOMEXgen()


def test_find_between():
    """Test the substring finding."""

    s = "SEDMLOMEXgen"
    first = "SEDML"
    last = "gen"
    substr = omexgen.find_between(s, first, last)
    assert substr == "OMEX"


def test_sbmltoantimony():
    """Test the SBML conversion to antimony string."""

    antimony_str = omexgen.sbmltoantimony(sbmlpath)
    model = re.search("model (.*)\n", antimony_str).group(1)
    assert model == "*gateNOT_d30_LB_state1_()"


def test_phrasedmltosedml(tmpdir):
    """Test the phrasedml string conversion SEDML."""

    path = os.path.join(str(tmpdir), "Testsedml.xml")
    sedml_str = omexgen.phrasedmltosedml(phrasedml_str, sbmlpath, outputfile=path)
    model = re.search('source="(.*)"', sedml_str).group(1)
    assert model == sbmlpath
    assert os.path.exists(path)


def test_exportomex(tmpdir):
    """Test the COMBINE OMEX file generation and exportation."""

    antimony_str = omexgen.sbmltoantimony(sbmlpath)

    path = os.path.join(str(tmpdir), "archive.omex")

    omex_str = omexgen.export_omex(antimony_str, phrasedml_str, outputfile=path)
    antimonymodel = re.search("model (.*)\n", omex_str).group(1)
    phrasedmlmodel = re.search('model1 = model "(.*)"', omex_str).group(1)
    phrasedmlmodel = "*" + phrasedmlmodel + "()"
    assert antimonymodel == phrasedmlmodel
    assert os.path.exists(path)


def test_getsbmlbiomodel(tmpdir):
    """Test getting SBML model from biomodel."""

    path = os.path.join(str(tmpdir), "Testbiomodel1.xml")
    biomodelsbml_str = omexgen.get_sbml_biomodel("BIOMD0000000012", outputfile=path)

    model = re.search(' id="(.*?)(")', biomodelsbml_str).group(1)
    assert model == "BIOMD0000000012"
    assert os.path.exists(path)
