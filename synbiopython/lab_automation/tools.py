# pylint: disable=C0116,C0103,E0401,W0631
"""Miscellaneous useful functions.

In particular, methods for converting to and from plate coordinates.
"""

import numpy as np


def round_at(value, rounding=None):
    """Round value at the nearest rounding.

    :param value: the value to round
    """
    if rounding is None:
        return value
    return np.round(value / rounding) * rounding


def replace_nans_in_dict(dictionary, replace_by="null"):
    """Replace NaNs in a dictionary with a string.

    :param dictionary: the dictionary
    :type dictionary: dict
    :param replace_by: replacement
    :type replace_by: str
    """
    for key, value in dictionary.items():
        if isinstance(value, dict):
            replace_nans_in_dict(value, replace_by=replace_by)
        elif value is np.nan:
            dictionary[key] = replace_by


def human_seq_size(n):
    "Return the given sequence as a human friendly 35b, 1.4k, 15k, etc."
    if n < 1000:
        return "%db" % n
    if n < 10000:
        return "%.1fk" % (n / 1000)

    return "%dk" % np.round(n / 1000)


unit_factors = {
    prefix + unit: factor
    for unit in "glL"
    for prefix, factor in [("", 1), ("m", 1e-3), ("u", 1e-6), ("n", 1e-9)]
}

volume_values_and_units = sorted(
    [(value, unit) for (unit, value) in unit_factors.items() if unit.endswith("L")]
)


def find_best_volume_unit(vols):
    """Find the best volume unit for a list of volumes."""
    med = np.median(vols)
    for value, unit in volume_values_and_units:
        if (not unit.endswith("g")) and (med <= 999 * value):
            return unit
    return unit


def human_volume(vol, unit="auto"):
    """Return a human-readable volume."""
    if unit == "auto":
        unit = find_best_volume_unit([vol])
    vol = np.round(vol / unit_factors[unit], 2)
    if int(vol) == vol:
        return "%d %s" % (vol, unit)

    return "%s %s" % (("%.02f" % vol).rstrip("0"), unit)
