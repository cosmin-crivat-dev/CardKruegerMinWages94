import importlib.util

import pandas as pd

from src.compute_variables import Test_FTE_and_GAP
from src.data_prep import NJPADataLoader


MODULE_PATH = "src/test_Regression_Adjusted Models.py"
SPEC = importlib.util.spec_from_file_location("regression_models", MODULE_PATH)
REGRESSION_MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REGRESSION_MODULE)
TestRegressionAdjustedModels = REGRESSION_MODULE.Test_Regression_Adjusted_Models


def test_generate_models_returns_requested_specifications():
    data_frame = Test_FTE_and_GAP().add_computed_columns(
        NJPADataLoader().load()
    )

    models = TestRegressionAdjustedModels().generate_models(data_frame)

    assert set(models) == {"1a", "1b"}
    assert "NJ" in models["1a"].model.exog_names
    assert "GAP" in models["1b"].model.exog_names
    assert "AE" in models["1a"].model.endog_names
    assert models["1a"].nobs > 0
    assert models["1b"].nobs > 0


def test_generate_models_requires_augmented_columns():
    data_frame = pd.DataFrame({"STATE": ["New Jersey"]})

    try:
        TestRegressionAdjustedModels().generate_models(data_frame)
    except ValueError as error:
        assert "FTE1" in str(error)
    else:
        raise AssertionError("Expected ValueError for incomplete data frame")


def test_show_model_coefficients_returns_table_4_style_values(capsys):
    data_frame = Test_FTE_and_GAP().add_computed_columns(
        NJPADataLoader().load()
    )
    regression_models = TestRegressionAdjustedModels()
    models = regression_models.generate_models(data_frame)

    table = regression_models.show_model_coefficients(models)

    assert list(table.columns) == ["(i)", "(ii)"]
    assert "New Jersey dummy" in table.index
    assert "Initial wage gap" in table.index
    assert "Standard error of regression" in table.index
    assert "R-squared" in table.index
    assert "(" in table.loc["New Jersey dummy", "(i)"]
    assert "TABLE 4" in capsys.readouterr().out