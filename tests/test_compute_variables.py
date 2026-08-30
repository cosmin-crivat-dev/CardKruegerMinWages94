import pandas as pd

from src.DiD_calculation import DiD_Calculation
from src.DiD_t_value_calculation import DiD_t_value_Calculation
from src.GAP_regression import GAP_Regression
from src.horse_race_regression import Horse_Race_Regression
from src.internal_DiD_calculation import internal_DiD_Calculation
from src.NJ_dummy_regression import NJ_Dummy_Regression
from src.standard_error_DiD_calculation import standard_error_DiD_Calculation
from src.test_FTE_and_GAP import Test_FTE_and_GAP, compute_fte1
from src.data_prep import NJPADataLoader


def test_compute_fte1_matches_formula():
    data_frame = pd.DataFrame(
        {
            "EMPFT": [10.0, 5.0],
            "NMGRS": [2.0, 1.0],
            "EMPPT": [8.0, 4.0],
        }
    )

    result = compute_fte1(data_frame)

    expected = pd.Series([16.0, 8.0], name="FTE1")
    pd.testing.assert_series_equal(result.reset_index(drop=True), expected)


def test_augmenter_adds_computed_columns_without_mutating_input():
    data_frame = NJPADataLoader().load()

    augmented = Test_FTE_and_GAP().add_computed_columns(data_frame)

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

    augmented = Test_FTE_and_GAP().add_computed_columns(data_frame)

    assert augmented.loc[0, "FTE1"] == 16.0
    assert augmented.loc[0, "FTE2"] == 16.0
    assert augmented.loc[0, "GAP"] == 0.2625


def test_computed_value_test_method_returns_requested_sample(capsys):
    data_frame = Test_FTE_and_GAP().add_computed_columns(
        NJPADataLoader().load()
    )

    sample = Test_FTE_and_GAP().test_computed_values(data_frame, rows=3)

    assert list(sample.columns) == ["SHEET", "STATE", "FTE1", "FTE2", "GAP"]
    assert len(sample) == 3
    assert "FTE1" in capsys.readouterr().out


def test_did_estimate_matches_state_changes():
    data_frame = NJPADataLoader().load()

    result = DiD_Calculation(data_frame)

    assert round(float(result["New Jersey"]), 4) == 0.5880
    assert round(float(result["Pennsylvania"]), 4) == -2.1656
    assert round(float(result["DiD"]), 4) == 2.7536


def test_internal_did_estimate_matches_low_and_high_wage_groups():
    data_frame = NJPADataLoader().load()

    result = internal_DiD_Calculation(data_frame)

    assert round(float(result["Low_wage_NJ"]), 4) == 0.7535
    assert round(float(result["High_wage_NJ"]), 4) == -4.0801
    assert round(float(result["internal_DiD"]), 4) == 4.8336


def test_standard_error_did_estimate_matches_sample_formula():
    data_frame = NJPADataLoader().load()

    result = standard_error_DiD_Calculation(data_frame)

    assert round(float(result["New Jersey_mean_change"]), 4) == 0.4667
    assert round(float(result["Pennsylvania_mean_change"]), 4) == -2.2833
    assert round(float(result["DiD_estimate"]), 4) == 2.7500
    assert round(float(result["DiD_standard_error"]), 4) == 1.3065


def test_did_t_statistic_matches_standard_error_formula():
    data_frame = NJPADataLoader().load()

    result = DiD_t_value_Calculation(data_frame)

    assert round(float(result["New Jersey_mean_change"]), 4) == 0.4667
    assert round(float(result["Pennsylvania_mean_change"]), 4) == -2.2833
    assert round(float(result["DiD_estimate"]), 4) == 2.7500
    assert round(float(result["DiD_standard_error"]), 4) == 1.3065
    assert round(float(result["DiD_t_statistic"]), 4) == 2.1048


def test_nj_dummy_regression_model_uses_state_dummy_and_controls():
    data_frame = NJPADataLoader().load()

    model = NJ_Dummy_Regression(data_frame)

    assert "NJ" in model.model.exog_names
    assert model.nobs == 351
    assert abs(model.params["NJ"] - 2.2815) < 0.05


def test_gap_regression_model_uses_gap_and_controls():
    data_frame = NJPADataLoader().load()

    model = GAP_Regression(data_frame)

    assert "GAP" in model.model.exog_names
    assert model.nobs == 351
    assert abs(model.params["GAP"] - 16.3631) < 0.5


def test_horse_race_regression_includes_both_nj_and_gap():
    data_frame = NJPADataLoader().load()

    model = Horse_Race_Regression(data_frame)

    assert "NJ" in model.model.exog_names
    assert "GAP" in model.model.exog_names
    assert model.nobs == 351
    assert abs(model.params["NJ"] - 0.8294) < 0.2
    assert abs(model.params["GAP"] - 14.0069) < 0.5