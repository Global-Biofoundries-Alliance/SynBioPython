# -*- coding: utf-8 -*-
""" Code to invoke the SBOL Validator server over the internet

@author: jingwui

This module provides code to work with SBOL validator
https://validator.sbolstandard.org/

Use sample sbol file from github (can also be obtained from iBioSim)
https://github.com/SynBioDex/SBOL-Validator/blob/master/src/test/sequence1.xml
https://www.w3schools.com/python/ref_requests_post.asp
http://synbiodex.github.io/SBOL-Validator/#query-parameters
http://synbiodex.github.io/SBOL-Validator/#options
http://biopython.org/DIST/docs/tutorial/Tutorial.html (Chapter 17 Graphics)
https://www.reportlab.com/
https://sbolstandard.org/visual/glyphs/ (SBOL visual glyphs)

install:
pip install biopython
pip install reportlab
The URI prefix is required for FASTA and GenBank conversion, and optional for SBOL 1 conversion
"""

import requests
import os

from Bio import SeqIO
from Bio.Graphics import GenomeDiagram
from reportlab.lib import colors
from reportlab.lib.units import cm


def Test_SBOL_Validator():

    # user input filename or path
    # input_filename = "sequence1.xml" # Test SBOL to others
    # input_file = "sequence2.gb" # Test GenBank to others
    input_file = "Testsequence1.gb"  # remove overlap sequence

    # Output = 'GenBank'
    # Output = 'FASTA'
    # Output = 'GFF3'
    # Output = 'SBOL1'
    Output = "SBOL2"

    # uri_Prefix = ''
    uri_Prefix = "http://synbiohub.org/public/igem"

    # This wrapper function takes in
    #  input_file: input file or path to input file
    #  Output: the Output file type (GenBank, FASTA, GFF3, SBOL1, SBOL2)
    #  uri_Prefix: '' as default, URI Prefix is required for FASTA and GenBank
    #              input conversion
    #  export output file in your folder
    #
    AutoRunSBOLValidator(input_file, Output, uri_Prefix)
    export_PlasmidMap(input_file)


def export_PlasmidMap(input_file):
    record = SeqIO.read(input_file, "genbank")

    gd_diagram = GenomeDiagram.Diagram(record.id)
    gd_track_for_features = gd_diagram.new_track(1, name="Annotated Features")
    gd_feature_set = gd_track_for_features.new_set()

    print(gd_feature_set)
    print(len(record))

    # print(record.features)

    # print(record.features)

    for feature in record.features:
        if feature.type != "CDS":

            # Exclude this feature
            continue
        if len(gd_feature_set) % 2 == 0:
            # print(gd_feature_set)
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

    print(gd_feature_set)

    # Draw Linear map from genbank
    gd_diagram.draw(
        format="linear",
        orientation="landscape",
        pagesize="A4",
        fragments=4,
        start=0,
        end=len(record),
    )
    gd_diagram.write("plasmid_linear.pdf", "PDF")
    gd_diagram.write("plasmid_linear.png", "PNG")

    # Draw circular map from genbank
    gd_diagram.draw(
        format="circular",
        circular=True,
        pagesize=(35 * cm, 30 * cm),
        start=0,
        end=len(record),
        circle_core=0.5,
    )
    gd_diagram.write("plasmid_circular.pdf", "PDF")


def SBOLValidator(input_file, Output, uri_Prefix=""):

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
    print(response.json())

    return response


# print(resp.json()['result'])

##
# get the output file extension based on the requested output language
##
def get_outputfile_extension(Filetype):
    switcher = {
        "GenBank": ".gb",
        "FASTA": ".fasta",
        "GFF3": ".gff",
        "SBOL1": ".sbol",
        "SBOL2": ".sbol",
    }
    return switcher.get(Filetype, "unknown filetype")


def export_OutputFile(input_filename, Response, Output):

    filename_w_ext = os.path.basename(input_filename)
    filename, file_extension = os.path.splitext(filename_w_ext)

    print(filename_w_ext)
    print(filename)

    if Response.json()["valid"]:
        # export the result from json into the specific output file format
        output_filename = filename + get_outputfile_extension(Output)
        print(output_filename)

        with open(output_filename, "w", newline="\n") as f:
            f.write(Response.json()["result"])
    else:
        print("Error message: ", Response.json()["errors"])


def AutoRunSBOLValidator(Input_file, Output, uri_Prefix=""):
    Response = SBOLValidator(Input_file, Output, uri_Prefix)
    export_OutputFile(Input_file, Response, Output)


# enable the script to be run from command line
if __name__ == "__main__":
    Test_SBOL_Validator()
