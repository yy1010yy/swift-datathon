# Independent routing review A

Question: Within each continuity flag and transaction route type, does the
reported participant count equal the count of visible BIC entries? Does treating
participants as distinct BICs instead change the result?

Population: every logical record of the cleaned gzip CSV. No anomaly exclusions,
deduplication, amount filtering, or imputations. Each record receives weight 1.

Parsing: split path on literal semicolons. A visible BIC matches exactly eight
uppercase alphanumeric characters; count literal `...` separately. Retain and
count any other token. Distinct visible BICs are a separate measure from visible
BIC entries. Do not interpret a gap as exactly one institution.

Reproducibility: run `.venv/Scripts/python.exe analysis/review_a.py` from the
project root. `route_counts.csv` stores joint counts, stratified by UTC month,
continuity, route, reported participants, entries, visible BIC entries, distinct
BICs, gaps, and other tokens. `summary.json` aggregates by flag/route and records
the label census. `examples.csv` is the first twelve encountered mismatches or
repeated-BIC paths, not a representative sample.

Uncertainty: a full-population identity is an observed identity in synthetic
data, not proof of the hidden generating program. BIC format checks do not
verify institution membership. UTC month replication tests temporal boundaries
but is not a prospective validation set because the question is descriptive.
