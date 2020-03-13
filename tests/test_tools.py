import pytest

import synbiopython.lab_automation as lab

wellname_data = [
    ("A5", "row", 5),
    ("A5", "column", 33),
    ("C6", "row", 30),
    ("C6", "column", 43),
]
inverted_wellname_data = [[s[-1], s[1], s[0]] for s in wellname_data]


@pytest.mark.parametrize("wellname, direction, expected", wellname_data)
def test_wellname_to_index(wellname, direction, expected):
    assert lab.Plate96().wellname_to_index(wellname, direction) == expected


@pytest.mark.parametrize("index, direction, expected", inverted_wellname_data)
def test_index_to_wellname(index, direction, expected):
    assert lab.Plate96().index_to_wellname(index, direction) == expected
