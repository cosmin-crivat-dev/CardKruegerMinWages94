import pandas as pd


def run_DiD_Calculation(data_frame: pd.DataFrame) -> pd.Series:
    """Return the DiD estimate from the New Jersey vs Pennsylvania employment changes."""
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


def DiD_Calculation_Print(data_frame: pd.DataFrame):
    """Print the New Jersey change, Pennsylvania change, and the DiD estimate."""
    estimates = run_DiD_Calculation(data_frame)
    print(f"New Jersey change: {estimates.loc['New Jersey']:.4f}")
    print(f"Pennsylvania change: {estimates.loc['Pennsylvania']:.4f}")
    print(f"DiD estimate: {estimates.loc['DiD']:.4f}")
