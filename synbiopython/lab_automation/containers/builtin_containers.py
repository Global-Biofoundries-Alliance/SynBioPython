"""Classes to represent plates"""
from synbiopython.lab_automation.containers.Plate import Plate
from synbiopython.lab_automation.containers.Well import Well


class Plate96(Plate):
    """Base class for standard 96-well plates"""

    num_rows = 8
    num_columns = 12


class Plate384(Plate):
    """Base class for standard 384-well plates"""

    num_rows = 16
    num_columns = 24


class Plate1536(Plate):
    """Base class for 1536-well plates (32 rows, 48 columns)"""

    num_rows = 32
    num_columns = 48


class Plate2x4(Plate):
    """Class for 8-well (2 x 4) plates such as colony plating plates"""

    num_rows = 2
    num_columns = 4


# Plate4ti0960


class Plate4ti0960Well(Well):
    """Well for 96-well plate from 4titude"""

    capacity = 150e-6


class Plate4ti0960(Plate96):
    """96-well plate from 4titude"""

    well_class = Plate4ti0960Well


# Plate4ti0130


class Plate4ti0130Well(Well):
    """Well for 96-well plate with 2ml deepwells from 4titude"""

    capacity = 1900e-6


class Plate4ti0130(Plate96):
    """96-well plate with 2ml deepwells from 4titude"""

    well_class = Plate4ti0130Well


# PlateLabcyteEchoLp0200Ldv


class PlateLabcyteEchoLp0200LdvWell(Well):
    """Well for low dead volume 384-well Echo plate"""

    capacity = 12e-6
    echo_dead_volume = 3e-6


class PlateLabcyteEchoLp0200Ldv(Plate384):
    """Low dead volume 384-well Echo plate"""

    class PlateWell(Well):
        """Well"""

        capacity = 12e-6
        echo_dead_volume = 3e-6


class PlateLabcyteEchoP05525Pp(Plate384):
    """Polypropylene 384-well ECHO plate"""

    class PlateWell(Well):
        """Well"""

        capacity = 50e-6
        echo_dead_volume = 15e-6


class Trough8x1(Plate):
    """Eight positions share the same content"""

    num_rows = 8
    num_columns = 1

    def __init__(self, name, wells_data=None, plate_data=None):
        Plate.__init__(self, name=name, wells_data=None, plate_data=None)
        for well in self:
            well.content = self["A1"].content
