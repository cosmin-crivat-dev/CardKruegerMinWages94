import pandas as pd
import statsmodels.formula.api as smf


def Horse_Race_Regression(data_frame: pd.DataFrame):
    """Estimate the horse-race regression: NJ and GAP compete in the same model."""
    data_frame = data_frame.copy()

    data_frame["FTE1"] = data_frame["EMPFT"] + data_frame["NMGRS"] + 0.5 * data_frame["EMPPT"]
    data_frame["FTE2"] = data_frame["EMPFT2"] + data_frame["NMGRS2"] + 0.5 * data_frame["EMPPT2"]
    data_frame["DIFF"] = data_frame["FTE2"] - data_frame["FTE1"]
    data_frame["NJ"] = (data_frame["STATE"] == "New Jersey").astype(int)
    data_frame["GAP"] = (
        ((5.05 - data_frame["WAGE_ST"]) / data_frame["WAGE_ST"])
        .where((data_frame["STATE"] == "New Jersey") & (data_frame["WAGE_ST"] < 5.05), 0.0)
    )

    regression_sample = data_frame.dropna(
        subset=["FTE1", "FTE2", "WAGE_ST", "WAGE_ST2", "CHAIN", "CO_OWNED", "STATE"]
    ).copy()

    model = smf.ols(
        "DIFF ~ NJ + GAP + CHAIN + CO_OWNED",
        data=regression_sample,
    ).fit()

    return model


def Horse_Race_Regression_Print():
    """Fit and print the horse-race regression results."""
    from src.data_prep import NJPADataLoader

    data_frame = NJPADataLoader().load()
    model = Horse_Race_Regression(data_frame)
    print(f"NJ coefficient: {model.params['NJ']:.4f}")
    print(f"GAP coefficient: {model.params['GAP']:.4f}")
    print(model.summary())
