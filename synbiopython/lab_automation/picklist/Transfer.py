# pylint: disable=C0103,C0330,C0114,C0115,C0116,C0301


class TransferError(ValueError):
    pass


class Transfer:
    """Class representing a transfer from a source well to a destination well.

    :param source_well: A Well object from which to transfer.
    :param destination_well: A Well object to which to transfer.
    :param volume: Volume to be transferred, expressed in liters.
    :param data: A dict containing any useful information about the transfer.
        This information can be used later e.g. as parameters for the transfer
        when exporting a picklist.
    """

    def __init__(self, source_well, destination_well, volume, data=None):

        self.volume = volume
        self.source_well = source_well
        self.destination_well = destination_well
        self.data = data

    def to_plain_string(self):
        """Return "Transfer {volume}L from {source_well} into {dest_well}"."""
        return (
            "Transfer {self.volume:.02E}L from {self.source_well.plate.name} "
            "{self.source_well.name} into "
            "{self.destination_well.plate.name} "
            "{self.destination_well.name}"
        ).format(self=self)

    def to_short_string(self):
        """Return "Transfer {volume}L {source_well} -> {dest_well}"."""
        return (
            "{self.__class__.__name__} {self.volume:.02E}L {self.source_well} -> {self.destination_well}"
        ).format(self=self)

    def with_new_volume(self, new_volume):
        """Return a version of the transfer with a new volume."""
        return self.__class__(
            source_well=self.source_well,
            destination_well=self.destination_well,
            volume=new_volume,
            data=self.data,
        )

    def apply(self):
        # error_prefix = "%s error:" % self.to_short_string()

        if self.source_well.is_empty:
            raise TransferError("Source well is empty!")

        #  pre-check in both source and destination wells that transfers
        #  are valid
        if self.volume > self.source_well.volume:
            raise TransferError(
                ("Subtraction of %.2e L from %s impossible." " Current volume: %.2e L")
                % (self.volume, self, self.source_well.volume)
            )
        final_destination_volume = self.destination_well.volume + self.volume
        if (self.destination_well.capacity is not None) and (
            final_destination_volume > self.destination_well.capacity
        ):
            raise TransferError(
                "Transfer of %.2e L from %s to %s brings volume over capacity."
                % (self.volume, self, self.destination_well)
            )

        #  If you arrive here, it means that the transfer is valid, do it.
        factor = float(self.volume) / self.source_well.volume

        quantities_transferred = {
            component: quantity * factor
            for component, quantity in self.source_well.content.quantities.items()
        }
        self.destination_well.add_content(quantities_transferred, volume=self.volume)
        self.source_well.subtract_content(quantities_transferred, volume=self.volume)
        if self not in self.destination_well.sources:
            self.destination_well.sources.append(self)

    def __repr__(self):
        """Return  "Transfer {volume}L from {source_well} into {dest_well}"."""
        return self.to_plain_string()
