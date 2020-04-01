import pytest
import os

import synbiopython.genbabel as stdgen

simplot = stdgen.SimpleDNAplot()

part_length = ["p0", "r0", "c0", "t0", "p1", "r1", "c1", "t1"]
part = "p1"


@pytest.mark.simplot
def test_dnalength():
    dnalength = simplot.ComputeDNALength(part, part_length)
    assert dnalength == 79.0


@pytest.fixture
def partlist():
    inputstr = "p.pTet c.orange.TetR"
    partlist, _ = simplot.CircuitDesign(inputstr)
    return partlist


@pytest.fixture
def regulations():
    inputstr = "p.pTet c.orange.TetR"
    regulation = "c0->p0.Repression.red"
    _, regulations = simplot.CircuitDesign(inputstr, regulation)
    return regulations


@pytest.mark.simplot
def test_inputstr(partlist):
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


@pytest.mark.simplot
def test_regulation(regulations):
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
    inputstr = "-c.orange.TetR -p.pTet"
    regulation = "c0->p0.Repression p0->p0.Derepression.red"
    _, regulations = simplot.CircuitDesign(inputstr, regulation)
    return regulations


@pytest.mark.simplot
def test_derepression(derepression):
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


@pytest.mark.simplot
def test_maxdnalength(tmpdir):
    figurepath = os.path.join(str(tmpdir), "check_PlotCircuit.png")
    Input = "p r c.green"
    dnalength = simplot.PlotCircuit(figurepath, Input, Regulation=None)
    assert dnalength == 60.0
    assert os.path.exists(figurepath)
