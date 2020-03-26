import pytest
import re
import os
import synbiopython.standardfile_generator as stdgen

path = os.path.abspath(os.path.dirname(__file__))
sbmlpath = r"data\gateNOT_d30_LB_state1_.xml"
filepath = os.path.join(path, sbmlpath)
phrasedml_str = """
      model1 = model "{}"
      sim1 = simulate uniform(0, 720, 1000)
      sim1.algorithm = rk4
      task1 = run sim1 on model1
      model2 = model model1 with state = 0
      task2 = run sim1 on model2
      plot "Fig 1: Pep (NOT gate 30C LB)" task1.time vs task1.Pep2, task2.Pep2
    """

omexgen = stdgen.SEDML_OMEXgen()


@pytest.mark.omexgen
def test_find_between():
    s = "SEDMLOMEXgen"
    first = "SEDML"
    last = "gen"
    substr = omexgen.find_between(s, first, last)
    assert substr == "OMEX"


@pytest.fixture
def sbmlfile():
    return filepath


@pytest.mark.omexgen
def test_sbmltoantimony(sbmlfile):
    antimony_str = omexgen.sbmltoantimony(sbmlfile)
    model = re.search("model (.*)\n", antimony_str).group(1)
    assert model == "*gateNOT_d30_LB_state1_()"


@pytest.mark.omexgen
def test_phrasedmltosedml():

    print(filepath)
    sedml_str = omexgen.phrasedmltosedml(phrasedml_str, filepath)
    model = re.search('source="(.*)"', sedml_str).group(1)
    assert model == filepath


@pytest.mark.omexgen
def test_exportomex(sbmlfile):
    antimony_str = omexgen.sbmltoantimony(sbmlfile)

    omex_str = omexgen.export_omex(antimony_str, phrasedml_str)
    antimonymodel = re.search("model (.*)\n", omex_str).group(1)
    phrasedmlmodel = re.search('model1 = model "(.*)"', omex_str).group(1)
    phrasedmlmodel = "*" + phrasedmlmodel + "()"
    assert antimonymodel == phrasedmlmodel


@pytest.mark.omexgen
def test_getsbmlbiomodel():
    biomodelsbml_str = omexgen.get_sbml_biomodel("BIOMD0000000012")
    model = re.search('<model id="(.*?)(")', biomodelsbml_str).group(1)
    assert model == "BIOMD0000000012"
