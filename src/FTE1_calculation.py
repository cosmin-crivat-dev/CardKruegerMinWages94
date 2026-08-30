import pandas as pd


def run_FTE1_Calculation(data_frame: pd.DataFrame) -> pd.Series:
    """Return the average FTE1 for New Jersey and Pennsylvania as a two-row Series."""
    data_frame["FTE1"] = data_frame["EMPFT"] + data_frame["NMGRS"] + 0.5 * data_frame["EMPPT"]

    averages = (
        data_frame.groupby("STATE")["FTE1"]
        .mean()
        .loc[["New Jersey", "Pennsylvania"]]
    )
    averages.name = "average_FTE1"
    return averages


def FTE_1_Calculation(data_frame: pd.DataFrame):
    """Print the average FTE1 values for New Jersey and Pennsylvania."""
    averages = run_FTE1_Calculation(data_frame)
    print(f"New Jersey average FTE1: {averages.loc['New Jersey']}")
    print(f"Pennsylvania average FTE1: {averages.loc['Pennsylvania']}")
