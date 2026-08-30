import pandas as pd


def DiD_t_value_Calculation(data_frame: pd.DataFrame) -> pd.Series:
    """Return the DiD point estimate, standard error, and t-statistic."""
    data_frame = data_frame.copy()
    data_frame["FTE1"] = data_frame["EMPFT"] + data_frame["NMGRS"] + 0.5 * data_frame["EMPPT"]
    data_frame["FTE2"] = data_frame["EMPFT2"] + data_frame["NMGRS2"] + 0.5 * data_frame["EMPPT2"]
    data_frame["DIFF"] = data_frame["FTE2"] - data_frame["FTE1"]

    nj_diff = data_frame.loc[data_frame["STATE"] == "New Jersey", "DIFF"]
    pa_diff = data_frame.loc[data_frame["STATE"] == "Pennsylvania", "DIFF"]

    nj_mean = float(nj_diff.mean())
    pa_mean = float(pa_diff.mean())
    did_estimate = nj_mean - pa_mean
    standard_error = (nj_diff.var(ddof=1) / len(nj_diff) + pa_diff.var(ddof=1) / len(pa_diff)) ** 0.5
    t_statistic = did_estimate / standard_error

    result = pd.Series(
        {
            "New Jersey_mean_change": nj_mean,
            "Pennsylvania_mean_change": pa_mean,
            "DiD_estimate": did_estimate,
            "DiD_standard_error": standard_error,
            "DiD_t_statistic": t_statistic,
        }
    )
    result.name = "DiD_t_value"
    return result


def DiD_t_value_Calculation_Print():
    """Print the DiD estimate, its standard error, and the t-statistic."""
    from src.data_prep import NJPADataLoader

    data_frame = NJPADataLoader().load()
    estimates = DiD_t_value_Calculation(data_frame)
    print(f"New Jersey mean change: {estimates.loc['New Jersey_mean_change']:.4f}")
    print(f"Pennsylvania mean change: {estimates.loc['Pennsylvania_mean_change']:.4f}")
    print(f"DiD estimate: {estimates.loc['DiD_estimate']:.4f}")
    print(f"DiD standard error: {estimates.loc['DiD_standard_error']:.4f}")
    print(f"DiD t-statistic: {estimates.loc['DiD_t_statistic']:.4f}")
