from pathlib import Path

import pandas as pd


class NJPADataLoader:
    """Load and label the New Jersey-Pennsylvania restaurant data set."""

    # These names follow the order and spelling in the supplied codebook.
    COLUMN_NAMES = [
        "SHEET", "CHAIN", "CO_OWNED", "STATE", "SOUTHJ", "CENTRALJ",
        "NORTHJ", "PA1", "PA2", "SHORE", "NCALLS", "EMPFT", "EMPPT",
        "NMGRS", "WAGE_ST", "INCTIME", "FIRSTINC", "BONUS", "PCTAFF",
        "MEALS", "OPEN", "HRSOPEN", "PSODA", "PFRY", "PENTREE", "NREGS",
        "NREGS11", "TYPE2", "STATUS2", "DATE2", "NCALLS2", "EMPFT2",
        "EMPPT2", "NMGRS2", "WAGE_ST2", "INCTIME2", "FIRSTIN2", "SPECIAL2",
        "MEALS2", "OPEN2R", "HRSOPEN2", "PSODA2", "PFRY2", "PENTREE2",
        "NREGS2", "NREGS112",
    ]

    # The codebook supplies labels for these numeric codes. Values not listed
    # in a mapping are left unchanged so unexpected source values are visible.
    CODE_MAPPINGS = {
        "CHAIN": {1: "Burger King", 2: "KFC", 3: "Roy Rogers", 4: "Wendy's"},
        "CO_OWNED": {0: "Franchise", 1: "Company-owned"},
        "STATE": {0: "Pennsylvania", 1: "New Jersey"},
        "BONUS": {0: "No", 1: "Yes"},
        "SPECIAL2": {0: "No", 1: "Yes"},
        "TYPE2": {1: "Phone", 2: "Personal"},
        "MEALS": {
            0: "None", 1: "Free meals", 2: "Reduced price meals",
            3: "Free and reduced price meals",
        },
        "MEALS2": {
            0: "None", 1: "Free meals", 2: "Reduced price meals",
            3: "Free and reduced price meals",
        },
        "STATUS2": {
            0: "Refused second interview",
            1: "Answered second interview",
            2: "Closed for renovations",
            3: "Closed permanently",
            4: "Closed for highway construction",
            5: "Closed due to Mall fire",
        },
    }

    # Every location indicator is documented as 1 if true and 0 otherwise.
    LOCATION_COLUMNS = ["SOUTHJ", "CENTRALJ", "NORTHJ", "PA1", "PA2", "SHORE"]

    def __init__(self, data_path=None):
        """Set the data path; by default use the project's bundled data file."""
        self.data_path = Path(data_path or Path(__file__).parent / "njmin" / "public.dat")

    def load(self, expand_codes=True):
        """Read public.dat into a DataFrame and optionally expand code values."""
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_path}")

        # The supplied file is whitespace-delimited and uses a dot for missing data.
        data_frame = pd.read_csv(
            self.data_path,
            sep=r"\s+",
            names=self.COLUMN_NAMES,
            na_values=".",
            keep_default_na=True,
            engine="python",
        )

        # DATE2 is stored as MMDDYY in the source and is more useful as a date.
        data_frame["DATE2"] = pd.to_datetime(
            data_frame["DATE2"].astype("Int64").astype("string"),
            format="%m%d%y",
            errors="coerce",
        )

        if expand_codes:
            data_frame = self.expand_codes(data_frame)

        return data_frame

    @classmethod
    def expand_codes(cls, data_frame):
        """Replace documented numeric codes with the full labels from the codebook."""
        expanded = data_frame.copy()

        for column, mapping in cls.CODE_MAPPINGS.items():
            expanded[column] = expanded[column].replace(mapping).astype("string")

        for column in cls.LOCATION_COLUMNS:
            expanded[column] = expanded[column].replace({0: "No", 1: "Yes"}).astype("string")

        return expanded


def compute_primary_statistics(data_frame):
    """Return one row of primary descriptive statistics for every column."""
    statistics = []

    for column in data_frame.columns:
        series = data_frame[column]
        column_statistics = {
            "column": column,
            "dtype": str(series.dtype),
            "non_null": int(series.notna().sum()),
            "missing": int(series.isna().sum()),
            "unique": int(series.nunique(dropna=True)),
            "mean": None,
            "std": None,
            "min": None,
            "max": None,
            "most_common": None,
            "most_common_count": None,
        }

        # Numeric columns receive the usual quantitative summary measures.
        if pd.api.types.is_numeric_dtype(series):
            column_statistics.update({
                "mean": series.mean(),
                "std": series.std(),
                "min": series.min(),
                "max": series.max(),
            })
        elif pd.api.types.is_datetime64_any_dtype(series):
            # Dates are summarized by their observed range instead of a mean.
            column_statistics.update({"min": series.min(), "max": series.max()})

        # Every type gets a mode so categorical and labeled columns are useful too.
        value_counts = series.value_counts(dropna=True)
        if not value_counts.empty:
            column_statistics["most_common"] = value_counts.index[0]
            column_statistics["most_common_count"] = int(value_counts.iloc[0])

        statistics.append(column_statistics)

    return pd.DataFrame(statistics)


def main():
    """Load the data and display its primary statistics."""
    data_frame = NJPADataLoader().load()
    print(f"Loaded {len(data_frame)} observations and {len(data_frame.columns)} columns.")
    primary_statistics = compute_primary_statistics(data_frame)
    print(primary_statistics.to_string(index=False))


if __name__ == "__main__":
    main()
