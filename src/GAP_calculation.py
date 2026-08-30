import pandas as pd


def GAP_Calculation(data_frame: pd.DataFrame) -> pd.Series:
    """Return average gap values for states, using the paper's NJ-below-minimum subset."""
    data_frame = data_frame.copy()

    new_jersey_below_minimum = (
        (data_frame["STATE"] == "New Jersey")
        & (data_frame["WAGE_ST"] < 5.05)
    )

    gap_values = pd.Series(0.0, index=data_frame.index, dtype="float64")
    gap_values.loc[new_jersey_below_minimum] = (
        ((5.05 - data_frame.loc[new_jersey_below_minimum, "WAGE_ST"]) /
         data_frame.loc[new_jersey_below_minimum, "WAGE_ST"]).round(4)
    )
    data_frame["GAP"] = gap_values

    nj_gap = data_frame.loc[new_jersey_below_minimum, "GAP"]
    pa_gap = data_frame.loc[data_frame["STATE"] == "Pennsylvania", "GAP"]

    averages = pd.Series(
        {
            "New Jersey": nj_gap.mean() if not nj_gap.empty else 0.0,
            "Pennsylvania": pa_gap.mean() if not pa_gap.empty else 0.0,
        }
    )
    averages.name = "average_GAP"
    return averages


def GAP_Calculation_Print():
    """Print the average GAP values for New Jersey and Pennsylvania."""
    from src.data_prep import NJPADataLoader

    data_frame = NJPADataLoader().load()
    averages = GAP_Calculation(data_frame)
    print(f"New Jersey average GAP: {averages.loc['New Jersey']:.4f}")
    print(f"Pennsylvania average GAP: {averages.loc['Pennsylvania']:.4f}")
