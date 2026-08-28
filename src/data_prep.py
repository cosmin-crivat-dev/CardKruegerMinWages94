"""Load and label the New Jersey-Pennsylvania minimum-wage data."""

from pathlib import Path

import pandas as pd


class NJPADataLoader:
    """Read ``public.dat`` using the layout documented in ``codebook``."""

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

    # These mappings are the numeric codes explicitly documented in codebook.
    CODE_MAPPINGS = {
        "CHAIN": {1: "Burger King", 2: "KFC", 3: "Roy Rogers", 4: "Wendy's"},
        "STATE": {0: "Pennsylvania", 1: "New Jersey"},
        "CO_OWNED": {0: "No", 1: "Yes"},
        "BONUS": {0: "No", 1: "Yes"},
        "SPECIAL2": {0: "No", 1: "Yes"},
        "SOUTHJ": {0: "No", 1: "Yes"},
        "CENTRALJ": {0: "No", 1: "Yes"},
        "NORTHJ": {0: "No", 1: "Yes"},
        "PA1": {0: "No", 1: "Yes"},
        "PA2": {0: "No", 1: "Yes"},
        "SHORE": {0: "No", 1: "Yes"},
        "MEALS": {
            0: "None",
            1: "Free meals",
            2: "Reduced price meals",
            3: "Free and reduced price meals",
        },
        "MEALS2": {
            0: "None",
            1: "Free meals",
            2: "Reduced price meals",
            3: "Free and reduced price meals",
        },
        "TYPE2": {1: "Phone", 2: "Personal"},
        "STATUS2": {
            0: "Refused second interview",
            1: "Answered second interview",
            2: "Closed for renovations",
            3: "Closed permanently",
            4: "Closed for highway construction",
            5: "Closed due to mall fire",
        },
    }

    def __init__(self, data_path: str | Path | None = None) -> None:
        """Set the input path, defaulting to the project's raw data location."""
        project_root = Path(__file__).resolve().parents[1]
        self.data_path = Path(data_path) if data_path else project_root / "raw" / "public.dat"

    def load(self, expand_codes: bool = True) -> pd.DataFrame:
        """Load the observations and optionally replace documented codes with labels."""
        input_path = self._available_data_path()
        data_frame = pd.read_csv(
            input_path,
            sep=r"\s+",
            names=self.COLUMN_NAMES,
            na_values=".",
            engine="python",
        )

        # DATE2 is stored as six digits in MMDDYY format in the flat file.
        data_frame["DATE2"] = pd.to_datetime(
            data_frame["DATE2"], format="%m%d%y", errors="coerce"
        )
        return self.expand_codes(data_frame) if expand_codes else data_frame

    def expand_codes(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """Return a copy with documented categorical codes expanded to full labels."""
        expanded = data_frame.copy()
        for column, mapping in self.CODE_MAPPINGS.items():
            if column in expanded:
                expanded[column] = expanded[column].map(mapping).combine_first(
                    expanded[column]
                )
        return expanded

    def _available_data_path(self) -> Path:
        """Use the expected raw path, or the repository's legacy bundled path."""
        if self.data_path.exists():
            return self.data_path
        legacy_path = self.data_path.parents[1] / "njmin" / self.data_path.name
        if legacy_path.exists():
            return legacy_path
        raise FileNotFoundError(f"Data file not found: {self.data_path}")