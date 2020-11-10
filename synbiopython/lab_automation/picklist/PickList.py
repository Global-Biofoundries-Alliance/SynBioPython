# pylint: disable=C0330,C0103,E0102,R1705,R0913
"""Classes to represent picklists and liquid transfers in general."""
from copy import deepcopy
from synbiopython.lab_automation.picklist.Transfer import Transfer


class PickList:
    """Representation of a list of well-to-well transfers.

    :param transfers_list: A list of Transfer objects that will be part of the same
        dispensing operation, in the order in which they are meant to be simulated.
    :param data: A dict with information on the picklist.
    """

    def __init__(self, transfers_list=(), data=None):

        self.transfers_list = list(transfers_list)
        self.data = {} if data is None else data

    def add_transfer(
        self,
        source_well=None,
        destination_well=None,
        volume=None,
        data=None,
        transfer=None,
    ):
        """Add a transfer to the picklist's tranfers list.

        You can either provide a ``Transfer`` object with the ``transfer``
        parameter, or the parameters.
        """
        if transfer is None:
            transfer = Transfer(
                source_well=source_well,
                destination_well=destination_well,
                volume=volume,
                data=data,
            )
        self.transfers_list.append(transfer)

    def to_plain_string(self):
        """Return the list of transfers in human-readable format."""
        return "\n".join(transfer.to_plain_string() for transfer in self.transfers_list)

    def to_plain_textfile(self, filename):
        """Write the picklist in a file in a human reable format."""
        with open(filename, "w+") as f:
            f.write(self.to_plain_string())

    def simulate(self, content_field="content", inplace=True):
        """Simulate the execution of the picklist."""

        if not inplace:
            all_plates = set(
                plate
                for transfer in self.transfers_list
                for plate in [
                    transfer.source_well.plate,
                    transfer.destination_well.plate,
                ]
            )
            new_plates = {plate: deepcopy(plate) for plate in all_plates}

            new_transfer_list = []
            for transfer in self.transfers_list:
                new_source_plate = new_plates[transfer.source_well.plate]
                new_dest_plate = new_plates[transfer.destination_well.plate]
                new_source_well = new_source_plate.wells[transfer.source_well.name]
                new_dest_well = new_dest_plate.wells[transfer.destination_well.name]
                new_transfer_list.append(
                    Transfer(
                        volume=transfer.volume,
                        source_well=new_source_well,
                        destination_well=new_dest_well,
                    )
                )

            new_picklist = PickList(transfers_list=new_transfer_list)
            new_picklist.simulate(
                content_field=content_field,
                inplace=True,
            )
            return new_plates

        else:
            for transfer in self.transfers_list:
                transfer.apply()
            return None

    def restricted_to(
        self, transfer_filter=None, source_well=None, destination_well=None
    ):
        """Return a version of the picklist restricted to transfers with the
        right source/destination well.

        You can provide ``source_well`` and ``destination_well`` or
        alternatively just a function ``transfer_filter`` with signature
        (transfer)=>True/False that will be used to filter out transfers
        (for which it returns false).
        """
        if transfer_filter is None:

            def transfer_filter(tr):
                source_well_is_ok = (source_well is None) or (
                    source_well == tr.source_well
                )
                dest_well_is_ok = (destination_well is None) or (
                    destination_well == tr.destination_well
                )
                return source_well_is_ok and dest_well_is_ok

        transfers = [tr for tr in self.transfers_list if transfer_filter(tr)]
        return PickList(transfers, data={"parent": self})

    def sorted_by(self, sorting_method="source_well"):
        """Return a new version of the picklist sorted by some parameter.

        The ``sorting_method`` is either the name of an attribute of the
        transfers, such as "source_well", or a function f(transfer) -> value.
        """
        if not hasattr(sorting_method, "__call__"):

            def sorting_method(transfer):
                return transfer.__dict__[sorting_method]

        return PickList(
            sorted(self.transfers_list, key=sorting_method),
            data={"parent": self},
        )

    def total_transferred_volume(self):
        """Return the sum of all volumes from all transfers."""
        return sum([transfer.volume for transfer in self.transfers_list])

    def enforce_maximum_dispense_volume(self, max_dispense_volume):
        """Return a new picklist were every too-large dispense is broken down
        into smaller dispenses."""
        transfers = []
        for trf in self.transfers_list:
            n_additional_dispense = int(trf.volume / max_dispense_volume)
            rest = trf.volume - n_additional_dispense * max_dispense_volume
            for _ in range(n_additional_dispense):
                transfers.append(trf.with_new_volume(max_dispense_volume))
            if rest > 0:
                transfers.append(trf.with_new_volume(rest))
        return PickList(transfers_list=transfers)

    def __add__(self, other):
        return PickList(self.transfers_list + other.transfers_list)

    @staticmethod
    def merge_picklists(picklists_list):
        """Merge the list of picklists into a single picklist.

        The transfers in the final picklist are the concatenation of the
        transfers in the different picklists, in the order in which they appear
        in the list.
        """
        return sum(picklists_list, PickList([]))
