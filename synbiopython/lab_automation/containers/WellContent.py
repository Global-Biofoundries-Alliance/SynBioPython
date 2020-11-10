# pylint: disable=C0103
"""This module contains a class to represent the volume and quantities of a well."""


class WellContent:
    """Class to represent the volume and quantities of a well.

    Having the well content represented as a separate object makes it possible
    to have several wells share the same content, e.g. in throughs.
    """

    def __init__(self, quantities=None, volume=0):
        if quantities is None:
            quantities = {}
        self.volume = volume
        self.quantities = quantities

    def concentration(self, component=None, default=0):
        """Return concentration of component."""
        if self.quantities == {}:
            return default
        if self.volume == 0:
            return default
        if component is None:
            component = list(self.quantities.keys())[0]
        if component not in self.quantities:
            return default
        return 1.0 * self.quantities[component] / self.volume

    def to_dict(self):
        """Return a dict {volume: 0.0001, quantities: {...:...}}."""
        return {"volume": self.volume, "quantities": self.quantities}

    def make_empty(self):
        """Empty the well."""
        self.volume = 0
        self.quantities = {}

    def components_as_string(self, separator=" "):
        """Return a string representation of what's in the well mix."""
        return separator.join(sorted(self.quantities.keys()))
