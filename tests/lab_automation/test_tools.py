import pytest

import numpy as np

from synbiopython.lab_automation import tools


def test_round_at():
    assert tools.round_at(42.0) == 42.0
    assert tools.round_at(6.28318, 10 ** (-2)) == 6.28


def test_dicts_to_columns():
    test_dict = {1: np.nan, 2: {"a": np.nan}}
    tools.replace_nans_in_dict(test_dict)
    expected = {1: "null", 2: {"a": "null"}}
    assert test_dict == expected


def test_human_seq_size():
    assert tools.human_seq_size(42) == "42b"
    tools.human_seq_size(1042) == "1.0k"
    tools.human_seq_size(42000) == "42k"


def test_human_volume():
    assert tools.human_volume(500) == "500 L"
