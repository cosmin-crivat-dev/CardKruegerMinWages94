import pandas as pd


def run_internal_DiD_Calculation(data_frame: pd.DataFrame) -> pd.Series:
    """Return the within-New Jersey internal DiD estimate using low- vs high-wage stores."""

    new_jersey = data_frame[data_frame["STATE"] == "New Jersey"].copy()
    below_minimum = new_jersey[new_jersey["WAGE_ST"] < 5.05]
    above_minimum = new_jersey[new_jersey["WAGE_ST"] >= 5.05]

    low_change = float(below_minimum["FTE2"].mean() - below_minimum["FTE1"].mean())
    high_change = float(above_minimum["FTE2"].mean() - above_minimum["FTE1"].mean())
    internal_did = low_change - high_change

    result = pd.Series(
        {
            "Low_wage_NJ": low_change,
            "High_wage_NJ": high_change,
            "internal_DiD": internal_did,
        }
    )
    result.name = "internal_DiD_estimate"
    return result


def internal_DiD_Calculation_Print(data_frame: pd.DataFrame):
    """Print the within-New Jersey internal DiD estimate."""
    estimates = run_internal_DiD_Calculation(data_frame)
    print(f"Low-wage NJ change: {estimates.loc['Low_wage_NJ']:.4f}")
    print(f"High-wage NJ change: {estimates.loc['High_wage_NJ']:.4f}")
    print(f"Internal DiD estimate: {estimates.loc['internal_DiD']:.4f}")
