class Transfer:
    """Class representing a tranfer from a source well to a destination well.

    Parameters
    ----------

    source_well
      A Well object representing the plate well from which to transfer

    destination_well
      A Well object representing the plate well to which to transfer.

    volume
      Volume to be transfered, expressed in liters.

    data
      A dict containing any useful information on the transfer, this
      information can be used later e.g. as parameters for the transfer
      when exporting a picklist.
    """
    def __init__(self, source_well, destination_well, volume, data=None):

        self.volume = volume
        self.source_well = source_well
        self.destination_well = destination_well
        self.data = data

    def to_plain_string(self):
        """Return "{volume}L from {source_well} to {dest_well}"."""
        return ("{self.volume:.02E}L from {self.source_well.plate.name} "
                "{self.source_well.name} into "
                "{self.destination_well.plate.name} "
                "{self.destination_well.name}").format(
                    self=self
        )
    def to_short_string(self):
        """Return "{volume}L from {source_well} to {dest_well}"."""
        return ("{self.__class__.__name__}({self.source_well}=>{self.dest_well}).plate.name} "
                "{self.source_well.name} into "
                "{self.destination_well.plate.name} "
                "{self.destination_well.name}").format(
                    self=self
        )

    def with_new_volume(self, new_volume):
        """Return a version of the transfer with a new volume."""
        return self.__class__(source_well=self.source_well,
                        destination_well=self.destination_well,
                        volume=new_volume,
                        data=self.data)
    
    def apply(self):
        error_prefix = "%s error:" % self.as_short_string()
        "%s impossible: %s is empty" % (
                 self, destination_well, self))
        if self.source_well.is_empty:
            raise TransferError(
                
        factor = float(transfer_volume) / self.volume

        #  pre-check in both source and destination wells that transfers
        #  are valid
        if factor > 1:
            raise TransferError(
                ("Substraction of %.2e L from %s impossible."
                 " Current volume: %.2e L")
                % (transfer_volume, self, self.volume)
            )
        final_destination_volume = destination_well.volume + transfer_volume
        if ((destination_well.capacity is not None) and
           (final_destination_volume > destination_well.capacity)):
            raise TransferError(
                "Transfer of %.2e L from %s to %s brings volume over capacity."
                % (transfer_volume, self, destination_well)
            )

        #  If you arrive here, it means that the transfer is valid, do it.
        quantities_transfered = {
            component: quantity * factor
            for component, quantity in self.content.quantities.items()
        }
        destination_well.add_content(quantities_transfered,
                                     volume=transfer_volume)
        self.subtract_content(quantities_transfered,
                              volume=transfer_volume)
        if self not in destination_well.sources:
            destination_well.sources.append(self)

    def __repr__(self):
        """Return "xx L from {source_well} into {dest_well}"."""
        return self.to_plain_string()

class TransferError(ValueError):
    pass

