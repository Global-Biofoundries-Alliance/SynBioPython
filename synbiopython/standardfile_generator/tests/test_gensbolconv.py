import pytest
import os
import synbiopython.standardfile_generator as stdgen

stdconv = stdgen.GenSBOLconv()
path = os.path.abspath(os.path.dirname(__file__))
sbolfile = "data/sequence1.xml"
sbolpath = os.path.join(path, sbolfile)
gbfile = "data/Testsequence1.gb"
gbpath = os.path.join(path, gbfile)
uri_Prefix_isbol = ""
uri_Prefix_igb = "http://synbiohub.org/public/igem"


@pytest.mark.stdconv
def test_sboltogb():
    Output = "GenBank"
    uri_Prefix = uri_Prefix_isbol
    Response = stdconv.AutoRunSBOLValidator(sbolpath, Output, uri_Prefix)
    assert Response == "valid: True"


@pytest.mark.stdconv
def test_sboltofasta():
    Output = "FASTA"
    uri_Prefix = uri_Prefix_isbol
    Response = stdconv.AutoRunSBOLValidator(sbolpath, Output, uri_Prefix)
    assert Response == "valid: True"


@pytest.mark.stdconv
def test_sboltogff3():
    Output = "GFF3"
    uri_Prefix = uri_Prefix_isbol
    Response = stdconv.AutoRunSBOLValidator(sbolpath, Output, uri_Prefix)
    assert Response == "valid: True"


@pytest.mark.stdconv
def test_gbtosbol():
    Output = "SBOL1"
    uri_Prefix = uri_Prefix_igb
    Response = stdconv.AutoRunSBOLValidator(gbpath, Output, uri_Prefix)
    assert Response == "valid: True"


@pytest.mark.stdconv
def test_gbtofasta():
    Output = "FASTA"
    uri_Prefix = uri_Prefix_igb
    Response = stdconv.AutoRunSBOLValidator(gbpath, Output, uri_Prefix)
    assert Response == "valid: True"


@pytest.mark.stdconv
def test_gbtogff3():
    Output = "FASTA"
    uri_Prefix = uri_Prefix_igb
    Response = stdconv.AutoRunSBOLValidator(gbpath, Output, uri_Prefix)
    assert Response == "valid: True"


@pytest.mark.stdconv
def test_export_PlasmidMap():
    recordid = stdconv.export_PlasmidMap(gbpath)
    assert recordid == "BBa_K874103.1"
