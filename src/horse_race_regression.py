import pandas as pd
import statsmodels.formula.api as smf


def run_Horse_Race_Regression(data_frame: pd.DataFrame):
    """Estimate the horse-race regression: NJ and GAP compete in the same model."""

    regression_sample = data_frame.dropna(
        subset=["FTE1", "FTE2", "WAGE_ST", "WAGE_ST2", "CHAIN", "CO_OWNED", "STATE"]
    ).copy()

    model = smf.ols(
        "DIFF ~ NJ + GAP + CHAIN + CO_OWNED",
        data=regression_sample,
    ).fit()

    return model


def Horse_Race_Regression_Print(data_frame: pd.DataFrame):
    """Fit and print the horse-race regression results."""
    model = run_Horse_Race_Regression(data_frame)
    print(f"NJ coefficient: {model.params['NJ']:.4f}")
    print(f"GAP coefficient: {model.params['GAP']:.4f}")
    print(model.summary())
