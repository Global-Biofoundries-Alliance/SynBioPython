import pytest

import synbiopython.lab_automation as lab
import synbiopython.lab_automation.containers.helper_functions as helper


def invert_sublists(l):
    return [sl[::-1] for sl in l]


@pytest.mark.parametrize(
    "num_wells, expected",
    [(48, (6, 8)), (96, (8, 12)), (384, (16, 24)), (1536, (32, 48))],
)
def test_compute_rows_columns(num_wells, expected):
    assert helper.compute_rows_columns(num_wells) == expected


rowname_data = [("A", 1), ("E", 5), ("AA", 27), ("AE", 31)]


@pytest.mark.parametrize("rowname, expected", rowname_data)
def test_rowname_to_number(rowname, expected):
    assert helper.rowname_to_number(rowname) == expected


@pytest.mark.parametrize("number, expected", invert_sublists(rowname_data))
def test_number_to_rowname(number, expected):
    assert helper.number_to_rowname(number) == expected


coordinates_data = [
    ("A1", (1, 1)),
    ("C2", (3, 2)),
    ("C04", (3, 4)),
    ("H11", (8, 11)),
    ("AA7", (27, 7)),
    ("AC07", (29, 7)),
]


@pytest.mark.parametrize("wellname, expected", coordinates_data)
def test_wellname_to_coordinates(wellname, expected):
    assert helper.wellname_to_coordinates(wellname) == expected


coord_to_name_data = [
    ((1, 1), "A1"),
    ((3, 2), "C2"),
    ((3, 4), "C4"),
    ((8, 11), "H11"),
    ((27, 7), "AA7"),
    ((29, 7), "AC7"),
]


@pytest.mark.parametrize("coords, expected", coord_to_name_data)
def test_coordinates_to_wellname(coords, expected):
    assert helper.coordinates_to_wellname(coords) == expected


wellname_data = [
    ("A5", 96, "row", 5),
    ("A5", 96, "column", 33),
    ("C6", 96, "row", 30),
    ("C6", 96, "column", 43),
    ("C6", 384, "row", 54),
    ("C6", 384, "column", 83),
]
inverted_wellname_data = [[s[-1], s[1], s[2], s[0]] for s in wellname_data]


@pytest.mark.parametrize("wellname, nwells, direction, expected", wellname_data)
def test_wellname_to_index(wellname, nwells, direction, expected):
    assert helper.wellname_to_index(wellname, nwells, direction) == expected
