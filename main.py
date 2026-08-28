import numpy as np
import pandas as pd
from pathlib import Path

from src.test_FTE_and_GAP import Test_FTE_and_GAP
from src.test_FTE_and_GAP import Test_Regression_Adjusted_Models    
from src.data_prep import NJPADataLoader

def main():
    """Load the New Jersey-Pennsylvania data frame."""
    data_frame = NJPADataLoader().load()

    # part 1 -- compute and test FTE* and GAP columns
    fte_gap_test = Test_FTE_and_GAP()
    data_frame = fte_gap_test.add_computed_columns(data_frame)
    fte_gap_test.test_computed_values(data_frame)

    ram_test = Test_Regression_Adjusted_Models()
    

if __name__ == "__main__":
    main()