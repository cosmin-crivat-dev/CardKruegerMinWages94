import pandas as pd
import statsmodels.formula.api as smf


def run_NJ_Dummy_Regression(data_frame: pd.DataFrame):
    """Estimate the New Jersey dummy model on the Table 4 sample restriction."""
    data_frame["NJ"] = (data_frame["STATE"] == "New Jersey").astype(int)

    regression_sample = data_frame.dropna(
        subset=["FTE1", "FTE2", "WAGE_ST", "WAGE_ST2", "CHAIN", "CO_OWNED", "STATE"]
    ).copy()

    model = smf.ols(
        "DIFF ~ NJ + CHAIN + CO_OWNED",
        data=regression_sample,
    ).fit()

    return model


def NJ_Dummy_Regression_Print(data_frame: pd.DataFrame):
    """Fit and print the New Jersey dummy regression results."""
    model = run_NJ_Dummy_Regression(data_frame)
    print(f"NJ dummy coefficient: {model.params['NJ']:.4f}")
    print(model.summary())
