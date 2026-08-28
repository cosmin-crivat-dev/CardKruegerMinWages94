import numpy as np
import pandas as pd


class Test_FTE_and_GAP:
    """Add derived employment and wage variables to the loaded data frame."""

    def add_computed_columns(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """Return a copy with the primary derived columns added."""
        augmented = data_frame.copy()

        # Full-time-equivalent employment includes half of part-time employment.
        augmented["FTE1"] = (
            augmented["EMPFT"]
            + augmented["NMGRS"]
            + 0.5 * augmented["EMPPT"]
        )
        augmented["FTE2"] = (
            augmented["EMPFT2"]
            + augmented["NMGRS2"]
            + 0.5 * augmented["EMPPT2"]
        )

        # GAP is the proportional increase needed to reach the NJ minimum wage.
        new_jersey_below_minimum = (
            (augmented["STATE"] == "New Jersey")
            & (augmented["WAGE_ST"] < 5.05)
        )
        augmented["GAP"] = np.select(
            [augmented["WAGE_ST"].isna(), new_jersey_below_minimum],
            [np.nan, (5.05 - augmented["WAGE_ST"]) / augmented["WAGE_ST"]],
            default=0,
        )
        return augmented

    def test_computed_values(
        self, data_frame: pd.DataFrame, rows: int = 5
    ):
        """Print computed values for inspection."""
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


        print("\nDifferences in FTe2 and FTE1 by state:")
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

