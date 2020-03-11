"""Miscellaneous useful functions.

In particular, methods for converting to and from plate coordinates.
"""

import numpy as np
from collections import OrderedDict
from fuzzywuzzy import process
import re


def round_at(value, rounding):
    """Round value at the nearest rounding"""
    if rounding is None:
        return value
    else:
        return np.round(value / rounding) * rounding


def dicts_to_columns(dicts):
    return {key: [d[key] for d in dicts] for key in dicts[0]}


def replace_nans_in_dict(dictionary, replace_by="null"):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            replace_nans_in_dict(value, replace_by=replace_by)
        elif value == np.nan:
            dictionary[key] = replace_by


def human_seq_size(n):
    "Return the given sequence as a human friendly 35b, 1.4k, 15k, etc."
    if n < 1000:
        return "%db" % n
    elif n < 10000:
        return "%.1fk" % (n / 1000)
    else:
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
    med = np.median(vols)
    for value, unit in volume_values_and_units:
        if (not unit.endswith("g")) and (med <= 999 * value):
            return unit
    return unit


def human_volume(vol, unit="auto"):
    if unit == "auto":
        unit = find_best_volume_unit([vol])
    vol = np.round(vol / unit_factors[unit], 2)
    if int(vol) == vol:
        return "%d %s" % (vol, unit)
    else:
        return "%s %s" % (("%.02f" % vol).rstrip("0"), unit)


def did_you_mean(name, other_names, limit=5, min_score=50):
    if isinstance(name, (list, tuple)):
        return {
            n: did_you_mean(n, other_names, limit=limit, min_score=min_score)
            for n in name
        }
    results = process.extract(name, list(other_names), limit=limit)
    return [e for (e, score) in results if score >= min_score]
