# console_app

A minimal Python console application.

## Run

```powershell
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
.venv\Scripts\python.exe main.py
```

## How It Works

The program in `main.py` performs these steps:

1. `NJPADataLoader` locates `njmin/public.dat` by default. A different file
	can be supplied when creating the loader.
2. The data file is read as whitespace-delimited data with the 46 column names
	listed in `njmin/codebook`.
3. Periods (`.`) in the source file are converted to pandas missing values
	(`NaN`).
4. `DATE2` is converted from the codebook's `MMDDYY` format to a date.
5. `expand_codes()` replaces documented numeric codes with readable labels,
	including restaurant chain, state, meal policy, interview type, interview
	status, and yes/no fields.
6. `compute_primary_statistics()` creates one summary row per column. Each row
	includes the data type, non-missing count, missing count, unique count,
	numeric mean, standard deviation, minimum, maximum, most common value, and
	most common value count. Measures that do not apply to a column are left
	blank.
7. `main()` loads the data, computes the statistics, and prints the complete
	46-row report to the console.

The bundled data set contains 410 observations. The loader can also be used
from another Python file:

```python
from main import NJPADataLoader, compute_primary_statistics

data_frame = NJPADataLoader().load()
statistics = compute_primary_statistics(data_frame)
```
