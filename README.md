# Datathon payment data

Initial EDA is now available in [analysis/initial_eda.ipynb](analysis/initial_eda.ipynb)
with executed code, results and charts. See [analysis/README.md](analysis/README.md)
for reproduction, [questions and theories](analysis/questions.md), and
[reviewed evidence and limits](analysis/progress.md). Current checklist: [AGENTS.md](AGENTS.md).

The source is a roughly 4.95 GB CSV, not an Excel workbook. It contains quoted
multiline fields, so physical line counts are not transaction counts. Avoid
opening the whole file in Excel or loading it into memory without chunking.

## Run the cleaning and profiling script

Create `.venv` on a fresh checkout using Python 3.10 or newer. The existing
environment uses Python 3.14.2:

```powershell
python -m venv .venv
```

Place the organizer-provided source CSV in the project root, or pass its location
with `--input`. The dataset, `.venv`, and generated `outputs/` are excluded from
Git and must be supplied or regenerated locally.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe clean_data.py --output-dir outputs/new_run
```

For a small trial:

```powershell
.\.venv\Scripts\python.exe clean_data.py --max-rows 10000 --chunk-size 4000 --output-dir outputs/my_trial
```

The default output directory is `outputs/cleaned`. Choose a new, empty output
directory when rerunning. The script refuses to replace an existing result.
The input file remains unchanged. A run that fails may leave partial output;
only a run that prints `Done` and writes `profile.json` and `data_overview.md`
is complete.

## What cleaning means here

- Lowercase column names and trim surrounding whitespace in structured fields.
- Uppercase currency, BIC and flag/type codes where appropriate.
- Extract the disclaimer to `dataset_disclaimer.txt`.
- Add a logical source record number, a UTC timestamp derived from epoch seconds,
  and semicolon-separated quality flags.
- Validate numeric fields, missing core values, BIC/currency formats and route
  consistency. Route checks are diagnostics whose business meaning needs review.
- Preserve every record, numeric source text, account identifier, multiline text,
  token field and blank anomaly label. Do not impute, deduplicate, winsorize or
  remove labeled anomalies.

There is no transaction ID, so repeated payments cannot safely be assumed to be
duplicates. Missing anomaly labels are not automatically interpreted as normal.
The case brief defines B as business, C as consumer, and TOTAL_DURATION in
seconds. The synthetic generator's token fields should be reviewed for
information leakage if building a model.

## Inspect the results

Start with `outputs/cleaned/data_overview.md`. The JSON profile contains exact
full-file category/missing/issue counts and streaming numeric summaries.
Floating-point numeric summaries are descriptive, not accounting reconciliation.
`column_profile.csv` and `category_counts.csv` provide compact tables.
`quality_issues.csv` links diagnostics to logical source record numbers.
`payments_sample.csv` contains the first 1,000 cleaned records for inspection;
it is not a random or representative sample.

The full result is `payments_cleaned.csv.gz`. Read it without unzipping:

```python
import pandas as pd

for chunk in pd.read_csv(
    "outputs/cleaned/payments_cleaned.csv.gz",
    chunksize=25_000,
    dtype="string",
    keep_default_na=False,
):
    # Preserve IDs/text and literal codes such as NA; convert selected numeric
    # columns explicitly when needed. Errors='coerce' requires checking failures.
    amounts = pd.to_numeric(chunk["usd_amount"], errors="coerce")
```

`anomaly_type` is a potential target label and must be excluded from model inputs.
Keep the source disclaimer with any derived data shared outside this folder.
