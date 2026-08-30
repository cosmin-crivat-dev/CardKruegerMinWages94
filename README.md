# CartKruegerMinWages94

This is a Python solution designed to verify the numeric analysis in a published paper.
The Python program replicates and verifies the paper calculations over the original data.


The paper is:

# Minimum Wages and Employment: A Case Study of the Fast-Food Industry in New Jersey and Pennsylvania

David Card and Alan B. Krueger

The American Economic Review
[Vol. 84, No. 4 (Sep., 1994)](https://www.jstor.org/stable/i337079), pp. 772-793 (22 pages)

The dataset is downloaded from https://davidcard.berkeley.edu/data_sets.html

The Python program replicates and verifies the paper calculations over the original data.

## Overview

This project reproduces the core empirical results from Card and Krueger's study on the effect of minimum wage increases on employment in the fast-food industry. The analysis uses the original New Jersey and Pennsylvania dataset and checks the paper's main numerical findings.

The program performs the following calculations:

- FTE1 and FTE2 full-time equivalent employment values
- GAP measure for wage changes relative to the minimum wage increase
- Difference-in-differences (DiD) estimate
- Internal DiD estimate
- DiD standard error
- DiD t-statistic
- NJ dummy regression
- GAP regression
- Horse-race regression including both NJ and GAP

## Project structure

- `main.py` loads the data and runs the full replication output
- `src/data_prep.py` loads and prepares the original dataset
- `src/*.py` contains the calculation and regression functions for each paper statistic
- `tests/` contains validation checks for the primary outputs

## Data source

The dataset is the original fast-food employment study data made available by David Card and Alan B. Krueger at:

https://davidcard.berkeley.edu/data_sets.html

The project uses the bundled `njmin` data files and codebook to reconstruct the variables used in the paper.

## Run the program

From the project root:

```powershell
.\.venv\Scripts\python.exe main.py
```

If needed, install dependencies first:

```powershell
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

## What the script prints

Running the program prints the paper-style summary statistics and model outputs, including:

- average employment by state
- GAP comparisons
- DiD and internal DiD estimates
- standard errors and t-statistics
- regression summaries for NJ dummy, GAP, and horse-race models

## Validation

The repository includes tests covering the core variable construction and regression outputs, so the replication can be checked against the paper's reported values.
