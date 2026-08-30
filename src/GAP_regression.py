import pandas as pd
import statsmodels.formula.api as smf


def run_GAP_Regression(data_frame: pd.DataFrame):
    """Estimate the wage-gap regression on the Table 4 sample restriction."""
    data_frame["GAP"] = (
        ((5.05 - data_frame["WAGE_ST"]) / data_frame["WAGE_ST"])
        .where((data_frame["STATE"] == "New Jersey") & (data_frame["WAGE_ST"] < 5.05), 0.0)
    )

    regression_sample = data_frame.dropna(
        subset=["FTE1", "FTE2", "WAGE_ST", "WAGE_ST2", "CHAIN", "CO_OWNED", "STATE"]
    ).copy()

    model = smf.ols(
        "DIFF ~ GAP + CHAIN + CO_OWNED",
        data=regression_sample,
    ).fit()

    return model


def GAP_Regression_Print(data_frame: pd.DataFrame):
    """Fit and print the wage-gap regression results."""
    model = run_GAP_Regression(data_frame)
    print(f"GAP coefficient: {model.params['GAP']:.4f}")
    print(model.summary())
