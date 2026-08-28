import numpy as np
import pandas as pd


class Test_FTE_and_GAP:
    """Add derived employment and wage variables to the loaded data frame."""

    def add_computed_columns(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """Return a copy with the primary derived columns added."""
        augmented = data_frame.copy()

        # Full-Time Equivalent is a way to statistically combine full-time and part-time headcounts into one number for each store. 
        # This is crucial to check because the entire paper is built on this variable and if it is incorrect it will cause a lot of problems later. 
        # (DiD, regressions) FTE1 is the first full-time equivalent employment as it is the data collected during the first survey before the minimum wage increase. 
        # The formula for FTE is: FTE1 = EMPFT + NMGRS + 0.5*EMPPT
        # EMPFT = Full-Time Employee    
        # EMPPT = Part-Time Employee
        # NMGRS = Number of Managers
        # They assumed each part-time employee as half a worker and assumes each part time employee contributes about half the labor of a full time employee
        # It may look like I am multiplying a list by a number but with pandas a Series allows me to apply an operation to every element inside of it. 
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

