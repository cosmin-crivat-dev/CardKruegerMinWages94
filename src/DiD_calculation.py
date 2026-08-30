import pandas as pd


def DiD_Calculation(data_frame: pd.DataFrame) -> pd.Series:
    """Return the DiD estimate from the New Jersey vs Pennsylvania employment changes."""
    data_frame = data_frame.copy()
    data_frame["FTE1"] = data_frame["EMPFT"] + data_frame["NMGRS"] + 0.5 * data_frame["EMPPT"]
    data_frame["FTE2"] = data_frame["EMPFT2"] + data_frame["NMGRS2"] + 0.5 * data_frame["EMPPT2"]

    group_means = data_frame.groupby("STATE")[["FTE1", "FTE2"]].mean()

    nj_change = float(group_means.loc["New Jersey", "FTE2"]) - float(group_means.loc["New Jersey", "FTE1"])
    pa_change = float(group_means.loc["Pennsylvania", "FTE2"]) - float(group_means.loc["Pennsylvania", "FTE1"])
    did_estimate = nj_change - pa_change

    result = pd.Series(
        {
            "New Jersey": nj_change,
            "Pennsylvania": pa_change,
            "DiD": did_estimate,
        }
    )
    result.name = "DiD_estimate"
    return result


def DiD_Calculation_Print():
    """Print the New Jersey change, Pennsylvania change, and the DiD estimate."""
    from src.data_prep import NJPADataLoader

    data_frame = NJPADataLoader().load()
    estimates = DiD_Calculation(data_frame)
    print(f"New Jersey change: {estimates.loc['New Jersey']:.4f}")
    print(f"Pennsylvania change: {estimates.loc['Pennsylvania']:.4f}")
    print(f"DiD estimate: {estimates.loc['DiD']:.4f}")
