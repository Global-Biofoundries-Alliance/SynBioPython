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


def test___repr__():
    assert (
        transfer.__repr__() == "Transfer 2.50E-05L from Source A1 into Destination B2"
    )
