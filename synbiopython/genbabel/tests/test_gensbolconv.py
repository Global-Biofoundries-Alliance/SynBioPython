import pytest
import os
import synbiopython.genbabel as stdgen

path = os.path.abspath(os.path.dirname(__file__))
sbolfile = "sequence1.xml"
sbolpath = os.path.join(path, "data", sbolfile)
gbfile = "Testsequence1.gb"
gbpath = os.path.join(path, "data", gbfile)
uri_Prefix_isbol = ""
uri_Prefix_igb = "http://synbiohub.org/public/igem"

stdconv = stdgen.GenSBOLconv()


@pytest.mark.stdconv
def test_sboltogb(tmpdir):
    path = os.path.join(str(tmpdir), sbolfile.split(".")[0] + ".gb")
    Output = "GenBank"
    uri_Prefix = uri_Prefix_isbol
    Response = stdconv.AutoRunSBOLValidator(
        sbolpath, Output, uri_Prefix, outputfile=path
    )
    print("tmppath: ", path)
    assert Response == "valid: True"
    assert os.path.exists(path)


@pytest.mark.stdconv
def test_sboltofasta(tmpdir):
    path = os.path.join(str(tmpdir), sbolfile.split(".")[0] + ".fasta")
    Output = "FASTA"
    uri_Prefix = uri_Prefix_isbol
    Response = stdconv.AutoRunSBOLValidator(
        sbolpath, Output, uri_Prefix, outputfile=path
    )
    assert Response == "valid: True"
    assert os.path.exists(path)


@pytest.mark.stdconv
def test_sboltogff3(tmpdir):
    path = os.path.join(str(tmpdir), sbolfile.split(".")[0] + ".gff")
    Output = "GFF3"
    uri_Prefix = uri_Prefix_isbol
    Response = stdconv.AutoRunSBOLValidator(
        sbolpath, Output, uri_Prefix, outputfile=path
    )
    assert Response == "valid: True"
    assert os.path.exists(path)


@pytest.mark.stdconv
def test_gbtosbol(tmpdir):
    path = os.path.join(str(tmpdir), gbfile.split(".")[0] + ".sbol")
    Output = "SBOL2"
    uri_Prefix = uri_Prefix_igb
    Response = stdconv.AutoRunSBOLValidator(gbpath, Output, uri_Prefix, outputfile=path)
    assert Response == "valid: True"
    assert os.path.exists(path)


@pytest.mark.stdconv
def test_gbtofasta(tmpdir):
    path = os.path.join(str(tmpdir), gbfile.split(".")[0] + ".fasta")
    Output = "FASTA"
    uri_Prefix = uri_Prefix_igb
    Response = stdconv.AutoRunSBOLValidator(gbpath, Output, uri_Prefix, outputfile=path)
    assert Response == "valid: True"
    assert os.path.exists(path)


@pytest.mark.stdconv
def test_gbtogff3(tmpdir):
    path = os.path.join(str(tmpdir), gbfile.split(".")[0] + ".gff")
    Output = "GFF3"
    uri_Prefix = uri_Prefix_igb
    # path = None
    Response = stdconv.AutoRunSBOLValidator(gbpath, Output, uri_Prefix, outputfile=path)
    assert Response == "valid: True"
    assert os.path.exists(path)
    # assert (Response == "valid: True")


@pytest.mark.stdconv
def test_export_PlasmidMap(tmpdir):
    path1 = os.path.join(str(tmpdir), "plasmid_linear.png")
    path2 = os.path.join(str(tmpdir), "plasmid_circular.png")
    recordid = stdconv.export_PlasmidMap(gbpath, (path1, path2))
    assert recordid == "BBa_K874103.1"
    assert os.path.exists(path1)
    assert os.path.exists(path2)
