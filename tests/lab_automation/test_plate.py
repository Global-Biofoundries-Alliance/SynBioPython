# pylint: disable=C0114,E0401,C0103,C0116,W0621
import pytest

import synbiopython.lab_automation as lab
from synbiopython.lab_automation.containers.Well import Well


def condition(well):
    return well.volume > 20 * 10 ** (-6)


def test_find_unique_well_by_condition():
    with pytest.raises(Exception):
        lab.Plate96().find_unique_well_by_condition(condition)


def test_find_unique_well_containing():
    with pytest.raises(Exception):
        lab.Plate96().find_unique_well_containing("testquery")


def test_list_well_data_fields():
    with pytest.raises(KeyError):
        lab.Plate96().list_well_data_fields()


def test_return_column():
    assert isinstance(lab.Plate96().return_column(5)[0], Well)
    assert len(lab.Plate96().return_column(5)) == 8


def test_list_wells_in_column():
    assert isinstance(lab.Plate96().list_wells_in_column(5)[0], Well)


def test_return_row():
    assert isinstance(lab.Plate96().return_row("A")[0], Well)
    assert isinstance(lab.Plate96().return_row(1)[0], Well)
    assert len(lab.Plate96().return_row("A")) == 12


def test_list_wells_in_row():
    assert isinstance(lab.Plate96().list_wells_in_row(5)[0], Well)


def test_list_filtered_wells():
    def condition(well):
        return well.volume > 50

    assert lab.Plate96().list_filtered_wells(condition) == []


def test_wells_grouped_by():
    assert len(lab.Plate96().wells_grouped_by()[0][1]) == 96


def test_get_well_at_index():
    well = lab.Plate96().get_well_at_index(5)
    assert well.name == "A5"


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


def test_iter_wells():
    result = lab.Plate96().iter_wells()
    assert isinstance(next(result), Well)


def test___repr__():
    assert lab.Plate96().__repr__() == "Plate96(None)"
