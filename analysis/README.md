# Reproducible initial EDA

Start with **[initial_eda.ipynb](initial_eda.ipynb)**. It includes the actual code and
executed outputs, not empty cells. Open it in VS Code or Jupyter; Python/Jupyter
is unnecessary just to read the JSON or the accompanying Markdown/CSV files.

- [questions.md](questions.md): prioritized questions, fields, comparisons, theories,
  counterexamples and status for every proposed feature group.
- [progress.md](progress.md): reviewed findings, limitations and next steps.
- [reviews/](reviews/): independent calculations, initial conclusions and debate.
- `../outputs/eda_initial/`: exact aggregate CSVs, manifest and two SVG charts.
- `../outputs/initial_eda_run.log`: captured execution output.

Run from the **project root** using the existing environment:

```powershell
.\.venv\Scripts\python.exe analysis/run_initial_eda.py > outputs/initial_eda_run.log 2>&1
.\.venv\Scripts\python.exe analysis/plot_initial_eda.py
.\.venv\Scripts\python.exe analysis/finalize_initial_eda.py
```

The first command streams all 10M records; allow several minutes and roughly a chunk's
memory. It replaces the initial-EDA aggregates/notebook, **never** the cleaned data.
Run the second command after the first succeeds; it adds the executed chart cell.
The third command verifies the independent review tables and appends its executed results;
it requires the saved A/B review tables (or rerun both reviewers first).
The notebook's cells can also run sequentially in a Python kernel from the project
root or `analysis/`. Only pandas/numpy are needed to regenerate it using the scripts.

Independent reviews can be reproduced from the root with `analysis/review_a.py`,
`analysis/review_b.py`, then `analysis/review_b_summary.py`. Debate documents record
human-readable review; computed comparison checks are in `analysis/verify_reviews.py`.

`outputs/` is ignored by Git; do not assume those tables travel with a checkout.
The executed notebook and small independent review artifacts live under `analysis/`
and can be shared with teammates. Keep the supplied dataset disclaimer with any
data-derived files shared outside this project. No raw account/detail text is copied
into the notebook. Example route CSVs expose synthetic BIC paths and record numbers.

The historical cleaning profile remains unchanged. Its limitation stating that duration
units and B/C meanings are undocumented is obsolete: the appendix defines seconds,
business and consumer. The EDA manifest records the correction. Existing quality flags
are preserved diagnostics, not proof of invalid data; see the reviewed routing result.
