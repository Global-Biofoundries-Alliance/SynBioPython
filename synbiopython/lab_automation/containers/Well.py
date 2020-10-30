# pylint: disable=C0330,C0103,R0913
"""This module contains a generic class for a well."""
from synbiopython.lab_automation.containers.WellContent import WellContent
from synbiopython.lab_automation.picklist.Transfer import TransferError
from ..tools import unit_factors


class Well:
    """Generic class for a well.

    :param plate: The plate on which the well is located
    :param row: The well's row (a number, starting from 0)
    :param column: The well's column (a number, starting from 0)
    :param name: The well's name, for instance "A1"
    :param data: A dictionary storing data on the well, used in algorithms and reports.
    """

    capacity = None
    dead_volume_per_transfer_class = None

    def __init__(self, plate, row, column, name, data=None):
        self.plate = plate
        self.row = row
        self.column = column
        self.name = name
        self.data = data or {}
        self.sources = []
        self.content = WellContent()

    @property
    def volume(self):
        """Return volume."""
        return self.content.volume

    def iterate_sources_tree(self):
        """Iterate through the tree of sources."""
        for source in self.sources:
            if isinstance(source, Well):
                for parent in source.iterate_sources_tree():
                    yield parent
            else:
                yield source
        yield self

    def add_content(self, components_quantities, volume=None, unit_volume="L"):
        """Add content to well.

        :param components_quantities: Dictionary of components and quantities
          (default: gram). Example `{"Compound_1": 5}`.
        :param volume: Volume (default: liter).
        :param unit_volume: Unit of volume (default: liter). Options: liter (L),
            milliliter (mL), microliter (uL), nanoliter (nL).
        """
        volume = volume * unit_factors[unit_volume]
        if volume > 0:
            final_volume = self.content.volume + volume
            if (self.capacity is not None) and (final_volume > self.capacity):
                raise TransferError(
                    "Transfer of %.2e L to %s brings volume over capacity."
                    % (volume, self)
                )
            self.content.volume = final_volume
        for component, quantity in components_quantities.items():
            if component not in self.content.quantities:
                self.content.quantities[component] = 0
            self.content.quantities[component] += quantity

    def subtract_content(self, components_quantities, volume=0):
        """Subtract content from well."""
        if volume > 0:
            if volume > self.volume:
                raise TransferError(
                    (
                        "Subtraction of %.2e L from %s is impossible."
                        " Current volume: %.2e L"
                    )
                    % (volume, self, self.volume)
                )
            self.content.volume -= volume
        for component, quantity in components_quantities.items():
            if self.content.quantities[component] == quantity:
                self.content.quantities.pop(component)
            else:
                self.content.quantities[component] -= quantity

    def empty_completely(self):
        """Empty the well."""
        self.content.quantities = {}
        self.content.volume = 0

    @property
    def coordinates(self):
        """Return (well.row, well.column)."""
        return (self.row, self.column)

    @property
    def is_empty(self):
        """Return true if the well's volume is 0."""
        return self.volume == 0

    def __repr__(self):
        return "(%s-%s)" % (self.plate.name, self.name)

    def pretty_summary(self):
        """Return a summary string of the well."""
        data = "\n    ".join(
            [""] + [("%s: %s" % (key, value)) for key, value in self.data.items()]
        )
        content = "\n    ".join(
            [""]
            + [
                ("%s: %s" % (key, value))
                for key, value in self.content.quantities.items()
            ]
        )
        return (
            "{self}\n"
            "  Volume: {self.volume}\n"
            "  Content: {content}\n"
            "  Metadata: {data}"
        ).format(self=self, content=content, data=data)

    def to_dict(self):
        """Convert well to dict"""
        return dict(
            [
                ["name", self.name],
                ["content", self.content.to_dict()],
                ["row", self.row],
                ["column", self.column],
            ]
            + list(self.data.items())
        )

    def index_in_plate(self, direction="row"):
        """Return the index of the well in the plate."""
        return self.plate.wellname_to_index(self.name, direction=direction)

    def is_after(self, other, direction="row"):
        """Return whether this well is located strictly after the other well.

        Example: iterate over all free wells after the last non-free well:

        >>> direction = 'row'
        >>> last_occupied_well = plate.last_nonempty_well(direction=direction)
        >>> free_wells = (w for w in plate.iter_wells(direction=direction)
        >>>               if w.is_after(last_occupied_well))
        >>> for well in free_wells: ...
        """
        well_index = self.index_in_plate(direction=direction)
        other_index = other.index_in_plate(direction=direction)
        return well_index > other_index

    def __lt__(self, other):
        return str(self) < str(other)
