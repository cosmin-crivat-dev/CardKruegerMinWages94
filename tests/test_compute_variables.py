import pandas as pd

from test_FTE_and_GAP import NJPAVariableAugmenter
from src.data_prep import NJPADataLoader


def test_augmenter_adds_computed_columns_without_mutating_input():
    data_frame = NJPADataLoader().load()

    augmented = NJPAVariableAugmenter().add_computed_columns(data_frame)

    assert list(data_frame.columns) == NJPADataLoader.COLUMN_NAMES
    assert {"FTE1", "FTE2", "GAP"}.issubset(augmented.columns)


def test_augmenter_computes_fte_values():
    data_frame = pd.DataFrame(
        {
            "EMPFT": [10.0],
            "NMGRS": [2.0],
            "EMPPT": [8.0],
            "EMPFT2": [12.0],
            "NMGRS2": [1.0],
            "EMPPT2": [6.0],
            "STATE": ["New Jersey"],
            "WAGE_ST": [4.0],
        }
    )

    augmented = NJPAVariableAugmenter().add_computed_columns(data_frame)

    assert augmented.loc[0, "FTE1"] == 16.0
    assert augmented.loc[0, "FTE2"] == 16.0
    assert augmented.loc[0, "GAP"] == 0.2625


def test_computed_value_test_method_returns_requested_sample(capsys):
    data_frame = NJPAVariableAugmenter().add_computed_columns(
        NJPADataLoader().load()
    )

    sample = NJPAVariableAugmenter().test_computed_values(data_frame, rows=3)

    assert list(sample.columns) == ["SHEET", "STATE", "FTE1", "FTE2", "GAP"]
    assert len(sample) == 3
    assert "FTE1" in capsys.readouterr().out