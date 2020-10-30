# pylint: disable=C0114,E0401,C0103,C0116
import pytest

import synbiopython.lab_automation as lab


def test_TransferError():
    with pytest.raises(ValueError):
        raise lab.TransferError()


source = lab.Plate96(name="Source")
destination = lab.Plate96(name="Destination")
source_well = source.wells["A1"]
destination_well = destination.wells["B2"]
volume = 25 * 10 ** (-6)
transfer = lab.Transfer(source_well, destination_well, volume)


def test_to_plain_string():
    assert (
        transfer.to_plain_string()
        == "Transfer 2.50E-05L from Source A1 into Destination B2"
    )


def test_to_short_string():
    assert (
        transfer.to_short_string()
        == "Transfer 2.50E-05L (Source-A1) -> (Destination-B2)"
    )


def test_with_new_volume():
    new_volume = 50 * 10 ** (-7)
    new_transfer = transfer.with_new_volume(new_volume)
    assert new_transfer.volume == new_volume


def test_apply():
    with pytest.raises(ValueError):
        transfer.apply()

    source_2 = lab.Plate96(name="Source_2")
    source_2.wells["A1"].add_content({"Compound_1": 1}, volume=5 * 10 ** (-6))
    destination_2 = lab.Plate96(name="Destination_2")
    transfer_2 = lab.Transfer(source_2.wells["A1"], destination_2.wells["B2"], volume)

    with pytest.raises(ValueError):
        transfer_2.apply()

    source_2.wells["A1"].add_content({"Compound_1": 1}, volume=25 * 10 ** (-6))
    destination_2.wells["B2"].capacity = 3 * 10 ** (-6)
    with pytest.raises(ValueError):
        transfer_2.apply()

    destination_2.wells["B2"].capacity = 50 * 10 ** (-6)
    transfer_2.apply()
    assert destination_2.wells["B2"].volume == volume


def test___repr__():
    assert (
        transfer.__repr__() == "Transfer 2.50E-05L from Source A1 into Destination B2"
    )
