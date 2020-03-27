import pytest
import re

import synbiopython.genbabel as stdgen

sbmlgen = stdgen.SBMLgen()

dx = "sigma *(y - x)"
dy = "rho*(z - y)"
dz = "beta*(y - z)"

ODE = [dx, dy, dz]
variable = ["x", "y", "z"]
Init = [0.8, 1.8, 19]
paramName = ["sigma", "rho", "beta"]
param = [20.0, 28, 3]
paramUnit = ["per_second", "per_second", "per_second"]


@pytest.mark.sbmlgen
def test_exportsbml():
    sbml = sbmlgen.exportsbml(ODE, variable, Init, paramName, param, paramUnit)
    specieslist = re.findall(r'species id="(.*?)"', sbml, re.MULTILINE)

    print(specieslist)

    assert specieslist == ["x", "y", "z"]
