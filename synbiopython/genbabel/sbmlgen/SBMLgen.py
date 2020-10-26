# pylint: disable=C0103,E0402,R0913,R0914,R0903,R0904,R0801
"""
Synbiopython (c) Global BioFoundry Alliance 2020

Synbiopython is licensed under the MIT License.

This module is to create SBML file for ODE model using simplesbml package,
which relies on libSBML.

Reference:
    https://github.com/sys-bio/simplesbml
"""

from synbiopython.genbabel.sbmlgen import simplesbml
from synbiopython.genbabel import utilities


class SBMLgen:
    """Class to generate SBML file for ODE model."""

    @staticmethod
    def export_sbml(ODE, Variable, Init, ParamName, Param, ParamUnit, **kwargs):
        """Function to generate the SBML xml file.

        :param ODE: The ODEs in the form of string stored in a list
        :type ODE: list
        :param Variable: The names of variable in a list of string
        :type Variable: list
        :param Init: Initial conditions for the variables in a list of values
        :type Init: list
        :param ParamName: The names of the parameters stored in a list
        :type ParamName: list
        :param Param: The parameters values
        :type Param: list
        :param ParamUnit: The unit for the parameter according to available unit definition
        :type ParamUnit: list
        :return: SBML in str
        :rtype: str
        """

        for u in ParamUnit:
            if u == "molL-1min-1":
                ParamUnit[ParamUnit.index(u)] = "molperLmin"
            elif u == "molL-1":
                ParamUnit[ParamUnit.index(u)] = "molperL"
            elif u == "s-1":
                ParamUnit[ParamUnit.index(u)] = "per_second"
            elif u == "min-1":
                ParamUnit[ParamUnit.index(u)] = "per_min"
            elif u == "dimensionless":
                ParamUnit[ParamUnit.index(u)] = "Dimension_less"
            else:
                print("Error in the defined units for parameters")

        model = simplesbml.sbmlModel()

        for s, _ in enumerate(Variable):
            model.addSpecies("[" + Variable[s] + "]", Init[s])

        for p, _ in enumerate(Param):
            model.addParameter(ParamName[p], Param[p], ParamUnit[p])

        for r, _ in enumerate(ODE):
            model.addRateRule(Variable[r], ODE[r])

        Model = model.toSBML()
        XMLfilename = "SBML_" + utilities.getfilename() + ".xml"
        output_file = XMLfilename
        for key, value in kwargs.items():
            if "outputfile" in key:
                output_file = value

        print(Model, file=open(output_file, "w"))
        return Model
