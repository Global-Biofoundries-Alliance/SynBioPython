# pylint: disable=C0114,C0103,C0116
import math
import re


def compute_rows_columns(num_wells):
    """Convert 96->(8,12), 384->(16,24), etc."""
    a = math.sqrt(num_wells / 6)
    n_rows = int(round(2 * a))
    n_columns = int(round(3 * a))
    return n_rows, n_columns


def rowname_to_number(name):
    "Convert A->1 Z->26 AA->27 etc."
    if len(name) == 2:
        return 26 * rowname_to_number(name[0]) + rowname_to_number(name[1])
    try:
        return "ABCDEFGHIJKLMNOPQRSTUVWXYZ".index(name) + 1
    except IndexError:
        raise ValueError(name + " is not a valid row name.")


def number_to_rowname(number):
    "Convert 1->A 26->Z 27->AA etc."
    if number > 26:
        return number_to_rowname(int(number / 26)) + number_to_rowname(number % 26)
    return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[number - 1]


def wellname_to_coordinates(wellname):
    """Convert A1->(1,1), H11->(8, 11), etc."""
    rowname, colname = re.match("([a-zA-Z]+)([0-9]+)", wellname).groups()
    return rowname_to_number(rowname), int(colname)


def coordinates_to_wellname(coords):
    """Convert (1,1)->A1, (4,3)->D3, (12, 12)->H12, etc."""
    row, column = coords
    return number_to_rowname(row) + str(column)


def wellname_to_index(wellname, num_wells, direction="row"):
    """Convert e.g. A1..H12 into 1..96
    direction is either row for A1 A2 A3... or column for A1 B1 C1 D1 etc.

    :param wellname: the name of the well
    :param num_wells: number of wells on the plate
    :type num_wells: int
    :param direction: the direction of counting. Either "row" or "column".
    :type direction: str
    """
    n_rows, n_columns = compute_rows_columns(num_wells)
    row, column = wellname_to_coordinates(wellname)
    if direction == "row":
        return column + n_columns * (row - 1)
    if direction == "column":
        return row + n_rows * (column - 1)
    raise ValueError("`direction` must be in (row, column)")


def index_to_row_column(index, num_wells, direction="row"):
    n_rows, n_columns = compute_rows_columns(num_wells)
    if direction == "row":
        row = 1 + int((index - 1) / n_columns)
        column = 1 + ((index - 1) % n_columns)
    elif direction == "column":
        row, column = 1 + ((index - 1) % n_rows), 1 + int((index - 1) / n_rows)
    else:
        raise ValueError("`direction` must be in (row, column)")
    return row, column


def index_to_wellname(index, num_wells, direction="row"):
    """Convert e.g. 1..96 into A1..H12

    :param index: the index of the well
    :type index: int
    :param num_wells: number of wells on the plate
    :type num_wells: int
    :param direction: the direction of counting. Either "row" or "column".
    :type direction: str
    """
    row, column = index_to_row_column(index, num_wells, direction)
    return coordinates_to_wellname((row, column))
