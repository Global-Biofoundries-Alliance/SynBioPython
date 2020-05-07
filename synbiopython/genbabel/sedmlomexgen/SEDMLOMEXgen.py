# pylint: disable=C0103,E0401
"""
Synbiopython (c) Global BioFoundry Alliance 2020

Synbiopython is licensed under the MIT License.

@author: yeohjingwui

"""

import os
import re
import tellurium as te
import tellurium.temiriam as temiriam
import matplotlib.pyplot as plt
import phrasedml
from synbiopython.genbabel import utilities

te.setDefaultPlottingEngine("matplotlib")

plt.close("all")

plt.rcdefaults()
plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.weight"] = "normal"
plt.rcParams["font.size"] = 11
plt.rcParams["axes.labelsize"] = 11
plt.rcParams["axes.labelweight"] = "normal"
plt.rcParams["axes.linewidth"] = 1
plt.rcParams["axes.formatter.limits"] = -3, 3
plt.rcParams["legend.frameon"] = False
params = {"mathtext.default": "regular"}
plt.rcParams.update(params)
plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False})


class SEDMLOMEXgen:
    """ Class to generate the SEDML and COMBINE OMEX files."""

    # get current working directory
    def __init__(self):

        self.workingdir0 = os.getcwd()

    def get_sbml_biomodel(self, Biomodels_ID, **kwargs):

        """ Get the ID for the Biomodels
        export the SBML model into .xml file
        return the sbml in string format
        """

        urn = "urn:miriam:biomodels.db:" + Biomodels_ID
        sbml_str = temiriam.getSBMLFromBiomodelsURN(urn=urn)

        # modify the format exported from Biomodel to the proper xml format
        sbml_str = sbml_str.replace("><", ">  <")  # for the last line
        sbml_str = sbml_str.replace(">  ", ">\n  ")
        sbml_str = sbml_str.replace("  </sbml", "</sbml")

        filepath = os.path.join(self.workingdir0, Biomodels_ID + ".xml")

        for key, value in kwargs.items():
            if "outputfile" in key:
                filepath = value

        with open(filepath, "wb") as f:
            f.write(sbml_str.encode("utf-8"))

        print("The SBML file path: ", filepath)

        return sbml_str

    @staticmethod
    def sbmltoantimony(sbmlfile):

        """Get the sbml file and return the antimony string """
        antimony_str = te.sbmlToAntimony(sbmlfile)
        basename = os.path.basename(sbmlfile)
        sbmlfilename = basename.split(".")[0]
        antimony_str = antimony_str.replace("doc0", sbmlfilename)

        return antimony_str

    @staticmethod
    def find_between(s, first, last):

        """Get the substring from string"""
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""

    def export_omex(self, antimony_str, phrasedml_str, **kwargs):

        """Take the antimony and phrasedml strings execute the omex and export into omex archive"""
        model = re.search("model (.*)\n", antimony_str)

        if model.group(1)[0] == "*":
            model = self.find_between(model.group(1), "*", "()")
            phrasedml_str = phrasedml_str.format(model)
        else:
            phrasedml_str = phrasedml_str.format(model.group(1))

        inline_omex = "\n".join([antimony_str, phrasedml_str])

        if "outputfile" in kwargs:
            filepath = kwargs["outputfile"]

        else:
            dirName = self.getOMEXfilename()

            try:
                os.mkdir(dirName)
                print("Directory ", dirName, " Created ")
            except FileExistsError:
                print("Directory ", dirName, " already exists")

            workingDir = os.path.join(self.workingdir0, dirName)

            filepath = os.path.join(workingDir, "archive.omex")

        print("The output file path: ", filepath)

        # execute the inline OMEX
        te.executeInlineOmex(inline_omex)

        te.exportInlineOmex(inline_omex, filepath)

        return inline_omex

    def phrasedmltosedml(self, phrasedml_str, sbml_file, **kwargs):

        """ take in phrasedml and sbml file in .xml, export the sedml.xml file,
        execute the sedml file, and return the sedml string
        Example of phrasedml_str:
            phrasedml_str = '''
            model1 = model "{}"
            .
            .
            '''
        """
        try:
            with open(sbml_file, "r+") as f:
                sbml_str = f.read()
        except IOError:
            print("Error in opening sbml file")

        phrasedml_str = phrasedml_str.format(sbml_file)

        phrasedml.setReferencedSBML(sbml_file, sbml_str)
        sedml_str = phrasedml.convertString(phrasedml_str)

        if sedml_str is None:
            raise RuntimeError(phrasedml.getLastError())

        sedml_file = os.path.join(self.workingdir0, "sedml.xml")

        for key, value in kwargs.items():
            if "outputfile" in key:
                sedml_file = value

        with open(sedml_file, "wb") as f:
            f.write(sedml_str.encode("utf-8"))

        return sedml_str

    @staticmethod
    def getOMEXfilename():

        """ return filename to the OMEX file according to the export time"""

        #        timenow = datetime.datetime.now()
        #
        #        year = str(timenow.year % 100)
        #        month = str(timenow.month).zfill(2)
        #        day = str(timenow.day).zfill(2)
        #        hour = str(timenow.hour).zfill(2)
        #        minute = str(timenow.minute).zfill(2)

        omexfilename = "OMEX" + utilities.getfilename()

        return omexfilename
