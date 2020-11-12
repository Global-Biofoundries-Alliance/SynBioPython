# pylint: disable=C0103,E0401,W0621
"""
Synbiopython (c) Global BioFoundry Alliance 2020

Synbiopython is licensed under the MIT License.

This module is the test file for the class SimpleDNAplot to be used for pytest
"""

import os
import pytest
import synbiopython.genbabel as stdgen

simplot = stdgen.SimpleDNAplot()

part_length = ["p0", "r0", "c0", "t0", "p1", "r1", "c1", "t1"]
part = "p1"


def test_dnalength():
    """Test the dnalength."""

    dnalength = simplot.compute_dnalength(part, part_length)
    assert dnalength == 79.0


@pytest.fixture
def partlist():
    """Return the partlist for testing."""

    inputstr = "p.pTet c.orange.TetR"
    Partlist, _ = simplot.set_circuit_design(inputstr)
    return Partlist


@pytest.fixture
def regulations():
    """Return the regulation for testing."""

    inputstr = "p.pTet c.orange.TetR"
    regulation = "c0->p0.Repression.red"
    _, Regulations = simplot.set_circuit_design(inputstr, regulation)
    return Regulations


def test_inputstr(partlist):
    """Test the dict list for the tested part list."""

    assert partlist == [
        {
            "name": "1",
            "type": "Promoter",
            "fwd": True,
            "opts": {
                "color": (0, 0, 0),
                "label": "pTet",
                "label_y_offset": -5,
                "label_color": "black",
                "label_size": 8,
                "label_style": "normal",
            },
        },
        {
            "name": "2",
            "type": "CDS",
            "fwd": True,
            "opts": {
                "color": (1.0, 0.5, 0.0),
                "label": "TetR",
                "label_y_offset": 0,
                "label_color": "white",
                "label_size": 10,
                "label_style": "italic",
            },
        },
    ]


def test_regulation(regulations):
    """Test the dict list for the regulations."""

    assert regulations == [
        {
            "type": "Repression",
            "from_part": {"start": 30.0, "end": 30.0},
            "to_part": {"start": 7.0, "end": 7.0, "fwd": False},
            "opts": {
                "color": (0.89, 0.1, 0.11),
                "linewidth": 1.5,
                "arc_height_const": 17,
                "arc_height_spacing": 4,
                "arc_height_start": 13,
                "arc_height_end": 13,
                "arc_height": 21,
                "arrowhead_length": 2,
            },
        }
    ]


@pytest.fixture
def derepression():
    """Return regulations for Derepression interaction."""

    inputstr = "-c.orange.TetR -p.pTet"
    regulation = "c0->p0.Repression p0->p0.Derepression.red"
    _, Regulations = simplot.set_circuit_design(inputstr, regulation)
    return Regulations


def test_derepression(derepression):
    """Test the dict list for the Derepression regulations"""

    assert derepression == [
        {
            "type": "Repression",
            "from_part": {"start": 16.0, "end": 16.0},
            "to_part": {"start": 39.0, "end": 39.0, "fwd": True},
            "opts": {
                "color": (0.0, 0.0, 0.0),
                "linewidth": 1.5,
                "arc_height_const": 17,
                "arc_height_spacing": -1,
                "arc_height_start": 13,
                "arc_height_end": 13,
                "arc_height": 16,
                "arrowhead_length": 2,
            },
        },
        {
            "type": "Repression",
            "from_part": {"start": 39.0, "end": 39.0},
            "to_part": {"start": 39.0, "end": 39.0, "fwd": True},
            "opts": {
                "color": (0.89, 0.1, 0.11),
                "linewidth": 1.5,
                "arc_height_const": 21.5,
                "arc_height_spacing": -1,
                "arc_height_start": 17.5,
                "arc_height_end": 17.5,
                "arc_height": 20.5,
                "arrowhead_length": 2,
            },
        },
    ]


def test_maxdnalength(tmpdir):
    """Test the maximum DNA length for the plotted gene circuit diagram."""

    figurepath = os.path.join(str(tmpdir), "check_PlotCircuit.png")
    Input = "p r c.green"
    dnalength, _ = simplot.plot_circuit(Input, Regulation=None, savefig=figurepath)
    assert dnalength == 60.0
    assert os.path.exists(figurepath)
