# pylint: disable=C0103,E0401,W0611
"""
Synbiopython (c) Global BioFoundry Alliance 2020

Synbiopython is licensed under the MIT License.

This module is the test file for the class SBMLgen to be used for pytest
"""

import os
import re
import pytest
import synbiopython.genbabel as stdgen
import synbiopython.genbabel.sbmlgen.simplesbml as simplesbml

sbmlgen = stdgen.SBMLgen()

""" Testing SBMLgen module """
dx = "sigma *(y - x)"
dy = "rho*(z - y)"
dz = "beta*(y - z)"

ODE = [dx, dy, dz]
variable = ["x", "y", "z"]
Init = [0.8, 1.8, 19]
paramName = ["sigma", "rho", "beta"]
param = [20.0, 28, 3]
paramUnit = ["s-1", "s-1", "s-1"]

""" Testing simplesbml module, adopted from simplesbml original module """
model = simplesbml.sbmlModel()
# Create new model
model.addSpecies("Glucose", 3.4)
# Add 3.4 moles of species 'Glucose'
model.addSpecies("[ATP]", 1.0)
# Add 1.0 M of species 'ATP' (in concentration instead of amount)
model.addSpecies("[G6P]", 0.0)
model.addSpecies("[ADP]", 0.0)
model.addParameter("k1", 0.1)
# Default units are 1/s
model.addParameter("fracATP", 1.0, units="dimensionless")
# For assignment rule later
model.addReaction(
    ["Glucose", "ATP"], ["2 G6P", "ADP"], "kp*Glucose*ATP", local_params={"kp": 0.1}
)
# Glucose+ATP -> 2G6P+ADP
model.addEvent("G6P == 1", {"k1": "0.3"})
# When [G6P] = 1 mol/L, k1 is reassigned as 0.3
model.addAssignmentRule("fracATP", "ATP/(ATP+ADP)")
# Parameter fracATP is equal to ATP/(ATP+ADP)


def test_export_sbml(tmpdir):
    """Test the SBML file generation and exportation."""

    path = os.path.join(str(tmpdir), "Testsbml.xml")
    sbml = sbmlgen.export_sbml(
        ODE, variable, Init, paramName, param, paramUnit, outputfile=path
    )
    specieslist = re.findall(r'species id="(.*?)"', sbml, re.MULTILINE)

    print(specieslist)

    assert specieslist == ["x", "y", "z"]
    assert os.path.exists(path)


def test_simplesbml(tmpdir):
    """Test the additional functions available inside the simplesbml."""

    code = simplesbml.writeCode(model.document)
    specieslist = re.findall(r"species_id='(.*?)'", code, re.MULTILINE)
    paramlist = re.findall(r"param_id='(.*?)'", code, re.MULTILINE)
    rxnlist = re.findall(r"expression='(.*?)'", code, re.MULTILINE)
    eventlist = re.findall(r"trigger='(.*?)'", code, re.MULTILINE)
    asglist = re.findall("var='(.*?)', math='(.*?)'", code, re.MULTILINE)

    path = os.path.join(str(tmpdir), "Testsimplesbml.xml")
    f1 = open(path, "w+")
    f1.write(model.toSBML())
    f1.close()

    assert specieslist == ["Glucose", "[ATP]", "[G6P]", "[ADP]"]
    assert paramlist == ["k1", "fracATP"]
    assert rxnlist == ["kp * Glucose * ATP"]
    assert eventlist == ["G6P == 1"]
    assert asglist == [("fracATP", "ATP / (ATP + ADP)")]
    assert os.path.exists(path)
