import pytest
import re
import os
import synbiopython.genbabel as stdgen

path = os.path.abspath(os.path.dirname(__file__))
sbmlfile = "gateNOT_d30_LB_state1_.xml"
sbmlpath = os.path.join(path, "data", sbmlfile)
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


@pytest.mark.omexgen
def test_find_between():
    s = "SEDMLOMEXgen"
    first = "SEDML"
    last = "gen"
    substr = omexgen.find_between(s, first, last)
    assert substr == "OMEX"


@pytest.mark.omexgen
def test_sbmltoantimony():
    antimony_str = omexgen.sbmltoantimony(sbmlpath)
    model = re.search("model (.*)\n", antimony_str).group(1)
    assert model == "*gateNOT_d30_LB_state1_()"


@pytest.mark.omexgen
def test_phrasedmltosedml(tmpdir):
    path = os.path.join(str(tmpdir), "Testsedml.xml")
    sedml_str = omexgen.phrasedmltosedml(phrasedml_str, sbmlpath, outputfile=path)
    model = re.search('source="(.*)"', sedml_str).group(1)
    assert model == sbmlpath
    assert os.path.exists(path)


@pytest.mark.omexgen
def test_exportomex(tmpdir):
    antimony_str = omexgen.sbmltoantimony(sbmlpath)

    path = os.path.join(str(tmpdir), "archive.omex")

    omex_str = omexgen.export_omex(antimony_str, phrasedml_str, outputfile=path)
    antimonymodel = re.search("model (.*)\n", omex_str).group(1)
    phrasedmlmodel = re.search('model1 = model "(.*)"', omex_str).group(1)
    phrasedmlmodel = "*" + phrasedmlmodel + "()"
    assert antimonymodel == phrasedmlmodel
    assert os.path.exists(path)


@pytest.mark.omexgen
def test_getsbmlbiomodel(tmpdir):
    path = os.path.join(str(tmpdir), "Testbiomodel.xml")
    biomodelsbml_str = omexgen.get_sbml_biomodel("BIOMD0000000012", outputfile=path)
    model = re.search('<model id="(.*?)(")', biomodelsbml_str).group(1)
    assert model == "BIOMD0000000012"
    assert os.path.exists(path)
