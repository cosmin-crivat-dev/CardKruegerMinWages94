import pandas as pd
import statsmodels.formula.api as smf


def NJ_Dummy_Regression(data_frame: pd.DataFrame):
    """Estimate the New Jersey dummy model on the Table 4 sample restriction."""
    data_frame = data_frame.copy()

    data_frame["FTE1"] = data_frame["EMPFT"] + data_frame["NMGRS"] + 0.5 * data_frame["EMPPT"]
    data_frame["FTE2"] = data_frame["EMPFT2"] + data_frame["NMGRS2"] + 0.5 * data_frame["EMPPT2"]
    data_frame["DIFF"] = data_frame["FTE2"] - data_frame["FTE1"]
    data_frame["NJ"] = (data_frame["STATE"] == "New Jersey").astype(int)

    regression_sample = data_frame.dropna(
        subset=["FTE1", "FTE2", "WAGE_ST", "WAGE_ST2", "CHAIN", "CO_OWNED", "STATE"]
    ).copy()

    model = smf.ols(
        "DIFF ~ NJ + CHAIN + CO_OWNED",
        data=regression_sample,
    ).fit()

    return model


def NJ_Dummy_Regression_Print():
    """Fit and print the New Jersey dummy regression results."""
    from src.data_prep import NJPADataLoader

    data_frame = NJPADataLoader().load()
    model = NJ_Dummy_Regression(data_frame)
    print(f"NJ dummy coefficient: {model.params['NJ']:.4f}")
    print(model.summary())
