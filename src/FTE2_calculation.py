import pandas as pd


def FTE2_Calculation(data_frame: pd.DataFrame) -> pd.Series:
    """Return the average FTE2 for New Jersey and Pennsylvania as a two-row Series."""
    data_frame = data_frame.copy()
    data_frame["FTE2"] = data_frame["EMPFT2"] + data_frame["NMGRS2"] + 0.5 * data_frame["EMPPT2"]

    averages = (
        data_frame.groupby("STATE")["FTE2"]
        .mean()
        .loc[["New Jersey", "Pennsylvania"]]
    )
    averages.name = "average_FTE2"
    return averages


def FTE_2calculation():
    """Print the average FTE2 values for New Jersey and Pennsylvania."""
    from src.data_prep import NJPADataLoader

    data_frame = NJPADataLoader().load()
    averages = FTE2_Calculation(data_frame)
    print(f"New Jersey average FTE2: {averages.loc['New Jersey']:.2f}")
    print(f"Pennsylvania average FTE2: {averages.loc['Pennsylvania']:.2f}")
