# pylint: disable=C0103,E0401
"""
Synbiopython (c) Global BioFoundry Alliance 2020

Synbiopython is licensed under the MIT License.

This module is the test file of the class GenSBOLconv for pytest
"""

import os
import pytest
import synbiopython.genbabel as stdgen

path0 = os.path.abspath(os.path.dirname(__file__))
sbolfile = "sequence1.xml"
sbolpath = os.path.join(path0, "data", sbolfile)
gbfile = "Testsequence1.gb"
gbpath = os.path.join(path0, "data", gbfile)
uri_Prefix_isbol = ""
uri_Prefix_igb = "http://synbiohub.org/public/igem"

stdconv = stdgen.GenSBOLconv()


@pytest.mark.stdconv
def test_sboltogb(tmpdir):
    """Test SBOL file conversion to Genbank file."""

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
    """Test SBOL file conversion to FASTA file."""

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
    """Test SBOL file conversion to GFF3 file."""

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
    """Test Genbank file conversion to SBOL file."""

    path = os.path.join(str(tmpdir), gbfile.split(".")[0] + ".sbol")
    Output = "SBOL2"
    uri_Prefix = uri_Prefix_igb
    Response = stdconv.AutoRunSBOLValidator(gbpath, Output, uri_Prefix, outputfile=path)
    assert Response == "valid: True"
    assert os.path.exists(path)


@pytest.mark.stdconv
def test_gbtofasta(tmpdir):
    """Test Genbank file conversion to FASTA."""

    path = os.path.join(str(tmpdir), gbfile.split(".")[0] + ".fasta")
    Output = "FASTA"
    uri_Prefix = uri_Prefix_igb
    Response = stdconv.AutoRunSBOLValidator(gbpath, Output, uri_Prefix, outputfile=path)
    assert Response == "valid: True"
    assert os.path.exists(path)


@pytest.mark.stdconv
def test_gbtogff3(tmpdir):
    """Test Genbank file conversion to GFF3."""

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
    """Test Plasmid Map Export function"""

    path1 = os.path.join(str(tmpdir), "plasmid_linear.png")
    path2 = os.path.join(str(tmpdir), "plasmid_circular.png")
    recordid = stdconv.export_PlasmidMap(gbpath, (path1, path2))
    assert recordid == "BBa_K874103.1"
    assert os.path.exists(path1)
    assert os.path.exists(path2)
