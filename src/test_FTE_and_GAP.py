import numpy as np
import pandas as pd


def compute_fte1(data_frame: pd.DataFrame) -> pd.Series:
    """Return the first survey full-time equivalent employment values."""
    values = (data_frame["EMPFT"] + data_frame["NMGRS"]) + 0.5 * data_frame["EMPPT"]
    values.name = "FTE1"
    return values


def compute_fte2(data_frame: pd.DataFrame) -> pd.Series:
    """Compute the second survey full-time equivalent employment."""
    values = (data_frame["EMPFT2"] + data_frame["NMGRS2"]) + 0.5 * data_frame["EMPPT2"]
    values.name = "FTE2"
    return values


def compute_gap(data_frame: pd.DataFrame) -> pd.Series:
    """Compute the New Jersey wage-gap measure for below-minimum stores."""
    new_jersey_below_minimum = (
        (data_frame["STATE"] == "New Jersey")
        & (data_frame["WAGE_ST"] < 5.05)
    )

    gap_values = pd.Series(np.nan, index=data_frame.index, dtype="float64")
    gap_values.loc[new_jersey_below_minimum] = (
        ((5.05 - data_frame.loc[new_jersey_below_minimum, "WAGE_ST"]) /
         data_frame.loc[new_jersey_below_minimum, "WAGE_ST"]).round(4)
    )
    return gap_values.fillna(0.0).rename("GAP")


class NJPAFTEGapComputation:
    """Add derived employment and wage variables to the loaded data frame."""
    __test__ = False

    def add_computed_columns(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """Return a copy with the primary derived columns added."""
        augmented = data_frame.copy()

        augmented["FTE1"] = compute_fte1(augmented)
        augmented["FTE2"] = compute_fte2(augmented)
        augmented["GAP"] = compute_gap(augmented)
        return augmented

    def test_computed_values(
        self, data_frame: pd.DataFrame, rows: int = 5
    ):
        """Print computed values for inspection."""

        # EMPFT has 6 missing values and EMPPT has 4 (out of 410 stores), so a small number of stores will have FTE1 = NaN. 
        # When computing .mean() by state, pandas automatically excludes these missing rows from the average (this is the default skipna=True behavior) 
        # rather than treating them as zero.
        # Now I must sort my results by state because Card and Kreuger took data from both New Jersey and Pennsylvania 
        # (they used Pennsylvania as a control group) 

        print("Results_FTE_and_GAP\n=====================")
        print("\nFTE1 mean:")
        print(data_frame.groupby("STATE")["FTE1"].mean())

        print("\nFTE2 mean:")
        print(data_frame.groupby("STATE")["FTE2"].mean())

        print("\nGAP mean:")
        print(data_frame.groupby("STATE")["GAP"].mean())

        print("\nGAP sum of non empty:")
        print(data_frame["GAP"].isna().sum())

        print("\nFTEs means:")
        group_means = data_frame.groupby("STATE")[["FTE1", "FTE2"]].mean()
        print(group_means)


        print("\n1.3 Change in Employment: Differences in FTE2 and FTE1 by state:")
        # Extract the difference between the mean FTE2 and FTE1 for each state
        nj_fte2 = float(group_means.loc["New Jersey", "FTE2"])
        nj_fte1 = float(group_means.loc["New Jersey", "FTE1"])
        pa_fte2 = float(group_means.loc["Pennsylvania", "FTE2"])
        pa_fte1 = float(group_means.loc["Pennsylvania", "FTE1"])
        nj_change = nj_fte2 - nj_fte1
        pa_change = pa_fte2 - pa_fte1
        did_estimate = nj_change - pa_change  # DiD estimate    


        print(f"NJ change: {nj_change}")
        print(f"PA change: {pa_change}")
        print(f"DiD estimate: {did_estimate}")

        sample = data_frame[["SHEET", "STATE", "FTE1", "FTE2", "GAP"]].head(rows)
        return sample


NJPAVariableAugmenter = NJPAFTEGapComputation
Test_FTE_and_GAP = NJPAFTEGapComputation
Test_FTE_and_GAP.__test__ = False

