# pylint: disable=C0114,E0401,C0103,C0116
import os

import pytest

import synbiopython.lab_automation as lab


source = lab.Plate96(name="Source")
destination = lab.Plate96(name="Destination")
source_well = source.wells["A1"]
destination_well = destination.wells["B2"]
volume = 25 * 10 ** (-6)
transfer_1 = lab.Transfer(source_well, destination_well, volume)
picklist = lab.PickList()


def test_add_transfer():
    picklist.add_transfer(transfer=transfer_1)
    assert isinstance(picklist.transfers_list[0], lab.Transfer)


def test_to_plain_string():
    assert (
        picklist.to_plain_string()
        == "Transfer 2.50E-05L from Source A1 into Destination B2"
    )


def test_to_plain_textfile(tmpdir):
    path = os.path.join(str(tmpdir), "test.txt")
    picklist.to_plain_textfile(filename=path)
    assert os.path.exists(path)


def test_simulate():
    with pytest.raises(ValueError):
        picklist.simulate(inplace=False)


def test_restricted_to():
    new_picklist = picklist.restricted_to(
        source_well=destination_well, destination_well=destination_well
    )
    assert len(new_picklist.transfers_list) == 0

    new_picklist_2 = picklist.restricted_to(
        source_well=source_well, destination_well=destination_well
    )
    assert len(new_picklist_2.transfers_list) == 1


def test_sorted_by():
    assert isinstance(lab.PickList().sorted_by(), lab.PickList)


def test_total_transferred_volume():
    assert picklist.total_transferred_volume() == 25 * 10 ** (-6)


def test_enforce_maximum_dispense_volume():
    new_picklist = picklist.enforce_maximum_dispense_volume(5 * 10 ** (-6))
    assert len(new_picklist.transfers_list) == 5


def test_merge_picklists():
    new_picklist = picklist.merge_picklists([picklist, picklist])
    assert len(new_picklist.transfers_list) == 2
