# pylint: disable=C0103,E0401
"""
Synbiopython (c) Global BioFoundry Alliance 2020

Synbiopython is licensed under the MIT License.

This module provides code to work with SBOL validator
https://validator.sbolstandard.org/

Use sample sbol file from github (can also be obtained from iBioSim)

Reference:
    https://github.com/SynBioDex/SBOL-Validator/blob/master/src/test/sequence1.xml
    http://synbiodex.github.io/SBOL-Validator/#query-parameters
    http://synbiodex.github.io/SBOL-Validator/#options
    http://biopython.org/DIST/docs/tutorial/Tutorial.html (Chapter 17 Graphics)

install:
    pip install biopython reportlab

The URI prefix is required for FASTA and GenBank conversion,
and optional for SBOL 1 conversion
"""

import os
import requests
from Bio import SeqIO
from Bio.Graphics import GenomeDiagram
from reportlab.lib import colors
from reportlab.lib.units import cm


class GenSBOLconv:
    """Class to convert standard files (SBOL1, SBOL2, GenBank, Fasta, GFF3)."""

    @staticmethod
    def export_plasmidmap(gbfile, filename=None):
        """ Export Linear and Circular Plasmid Map for the imported GenBank file.

        :param gbfile: a genbank file in .gb format or the path the file if not in the
            same folder.
        :type gbfile: str
        :param filename: the filenames/path to the filenames for the linear and
            circular plasmids in tuple
        :type filename: tuple, optional
        :return: the version from the genbank file
        :rtype: str
        """

        record = SeqIO.read(gbfile, "genbank")

        gd_diagram = GenomeDiagram.Diagram(record.id)
        gd_track_for_features = gd_diagram.new_track(1, name="Annotated Features")
        gd_feature_set = gd_track_for_features.new_set()

        for feature in record.features:
            if feature.type == "primer" or (feature.type == "misc_feature"):
                continue
            #            if (feature.type != "CDS"):
            #                # Exclude this feature
            #                continue
            if len(gd_feature_set) % 2 == 0:
                color = colors.lightblue

            else:
                color = colors.blue

            gd_feature_set.add_feature(
                feature,
                sigil="ARROW",
                color=color,
                label_size=12,
                label_angle=0,
                label=True,
            )

        # Draw Linear map from genbank
        gd_diagram.draw(
            format="linear",
            orientation="landscape",
            pagesize="A4",
            fragments=4,
            start=0,
            end=len(record),
        )
        if filename is None:
            linfile = "plasmid_linear.png"
            circfile = "plasmid_circular.png"
        else:
            linfile = filename[0]
            circfile = filename[1]

        gd_diagram.write(linfile, "PNG")

        # Draw circular map from genbank
        gd_diagram.draw(
            format="circular",
            circular=True,
            pagesize=(25 * cm, 20 * cm),  # pagesize=(35 * cm, 30 * cm),
            start=0,
            end=len(record),
            circle_core=0.5,
        )
        # gd_diagram.write("plasmid_circular.pdf", "PDF")
        gd_diagram.write(circfile, "PNG")

        return record.id

    @staticmethod
    def access_sbolvalidator(input_file, Output, uri_Prefix=""):
        """Code to invoke the SBOL Validator server over the internet.

        :param input_file: input filename or filepath
        :type input_file: str
        :param Output: the type of Output file
        :type Output: str, ('GenBank', 'FASTA', 'GFF3', 'SBOL1', 'SBOL2')
        :param uri_Prefix: '' as default, URI Prefix is required for FASTA and GenBank
            input conversion
        :type uri_Prefix: str, optional
        :return: POST request response from webpage
        :rtype: object
        """

        file = open(input_file).read()

        request = {
            "options": {
                "language": Output,
                "test_equality": False,
                "check_uri_compliance": False,
                "check_completeness": False,
                "check_best_practices": False,
                "fail_on_first_error": False,
                "provide_detailed_stack_trace": False,
                "subset_uri": "",
                "uri_prefix": uri_Prefix,
                "version": "",
                "insert_type": False,
                "main_file_name": "main file",
                "diff_file_name": "comparison file",
            },
            "return_file": True,
            "main_file": file,
        }

        # send POST request to the specified url (Response [200] means ok)
        response = requests.post(
            "https://validator.sbolstandard.org/validate/", json=request
        )

        return response

    @staticmethod
    def get_outputfile_extension(Filetype):
        """Get the output file extension based on the requested output language.

        :param Filetype: the type of Output file
        :type Output: str, ('GenBank', 'FASTA', 'GFF3', 'SBOL1', 'SBOL2')
        :return: the specific file extension
        :rtype: str
        """

        switcher = {
            "GenBank": ".gb",
            "FASTA": ".fasta",
            "GFF3": ".gff",
            "SBOL1": ".sbol",
            "SBOL2": ".sbol",
        }
        return switcher.get(Filetype, "unknown filetype")

    def export_outputfile(self, input_filename, Response, Output, outputfile=None):
        """Export the converted output file.

        :param input_filename: input filename or filepath
        :type input_filename: str
        :param Response: response from POST request to sbolvalidator web page
        :type Response: object
        :param Output: the type of Output file
        :type Output: str, ('GenBank', 'FASTA', 'GFF3', 'SBOL1', 'SBOL2')
        :param outputfile: provide specific outputfilename or filepath
        :type outputfile: str, optional
        """

        filename_w_ext = os.path.basename(input_filename)
        filename, _ = os.path.splitext(filename_w_ext)

        if Response.json()["valid"]:
            # export the result from json into the specific output file format
            if outputfile is None:
                output_filename = filename + self.get_outputfile_extension(Output)
            else:
                output_filename = outputfile

            print("Output file: ", output_filename)

            with open(output_filename, "w", newline="\n") as f:
                f.write(Response.json()["result"])
        else:
            print("Error message: ", Response.json()["errors"])

    def run_sbolvalidator(self, Input_file, Output, uri_Prefix="", **kwargs):
        """Wrapper function for the SBOL Validator.

        :param Input_file: input file or path to input file
        :type Input_file: str, filename or filepath
        :param Output: the type of Output file
        :type Output: str, ('GenBank', 'FASTA', 'GFF3', 'SBOL1', 'SBOL2')
        :param uri_Prefix: '' as default, URI Prefix is required for FASTA and GenBank
            input conversion
        :type uri_Prefix: str, optional
        :return: the validity of the Response, and export output file.
        :rtype: str, "valid: True" if the conversion is done properly
        :Keyword Arguments:
            * *outputfile*: specify outputfile
        """
        Response = self.access_sbolvalidator(Input_file, Output, uri_Prefix)

        output_filename = None

        for key, value in kwargs.items():
            if "outputfile" in key:
                output_filename = value

        self.export_outputfile(Input_file, Response, Output, outputfile=output_filename)

        return "valid: " + str(Response.json()["valid"])
