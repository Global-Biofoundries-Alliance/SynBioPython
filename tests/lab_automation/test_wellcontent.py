# pylint: disable=C0114,E0401,C0103,C0116,W0621
from synbiopython.lab_automation.containers.WellContent import WellContent

wellcontent = WellContent(
    quantities={"Compound_1": 5, "Compound_2": 10}, volume=25
)  # 30 L [sic]


def test_concentration():
    assert WellContent().concentration() == 0
    assert WellContent(quantities={"Compound_1": 5}).concentration() == 0

    assert wellcontent.concentration() == 0.2
    assert wellcontent.concentration("Compound_1") == 0.2
    assert wellcontent.concentration("Compound_2") == 0.4
    assert wellcontent.concentration("Compound_3") == 0  # not in wellcontent


def test_to_dict():
    result = wellcontent.to_dict()
    expected = {"volume": 25, "quantities": {"Compound_1": 5, "Compound_2": 10}}
    assert result == expected


def test_make_empty():
    wellcontent = WellContent(quantities={"Compound_1": 5, "Compound_2": 10}, volume=25)
    wellcontent.make_empty()
    assert wellcontent.volume == 0
    assert wellcontent.quantities == {}


def test_components_as_string():
    assert wellcontent.components_as_string() == "Compound_1 Compound_2"
