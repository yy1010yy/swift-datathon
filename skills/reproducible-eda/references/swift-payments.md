# Swift payments project context

Read when using this skill for the UMDAC 2026 Swift datathon. Resolve all project
paths against the active checkout; do not assume a specific Windows username.

## Inputs and authoritative meanings

- Cleaned payments: `outputs/cleaned/payments_cleaned.csv.gz`.
- Full profile: `outputs/cleaned/profile.json`; first-1,000 preview is not random.
- Original cleaner: `clean_data.py`. It preserves all 10,000,000 supplied rows.
- The case brief linked in `AGENTS.md`, appendix pp. 3–4, defines fields. Use only
  supplied payment data as evidence for reconstructed rules; illustrative GDP and
  currency-letter examples in the brief are not findings.
- `total_duration` is seconds. `usd_amount` is USD-normalized. B means business;
  C means consumer. Tokens derive from the corresponding raw detail text.
- `bic8_path` is semicolon-delimited. Literal `...` is a gap, not a bank. Count
  visible BIC occurrences, distinct visible BICs and gap entries separately.
- Blank `anomaly_type` means no recorded anomaly label, not proven legitimate.
- Preserve repeated directed account-pair edges. There is no unique transaction ID.
  A repeated record is not automatically an accidental duplicate.
- The synthetic population's country shares do not estimate real-world market shares.

The historical profile has a stale limitation saying duration and B/C meanings are
undocumented. Preserve that original artifact; use the appendix and record corrections
alongside each new analysis. Do not silently rewrite old results.

## Existing work to inspect before continuing

- `analysis/initial_eda.ipynb`: seven executed blocks, outputs and two charts.
- `analysis/questions.md`: prioritized questions, proposed theories and challenges.
- `analysis/progress.md`: reviewed wording, supporting figures, boundaries and next work.
- `analysis/README.md`: reproduction commands and artifact-sharing notes.
- `analysis/run_initial_eda.py`, `plot_initial_eda.py`, `finalize_initial_eda.py`:
  produce aggregates, notebook, charts and verification outputs, respectively.
- `analysis/review_a.py`, `review_b.py`, `review_b_summary.py`, `verify_reviews.py`:
  independent full-file scans and exact cross-review comparison.
- `analysis/reviews/a/` and `analysis/reviews/b/`: initial conclusions, debate and tables.
- `outputs/eda_initial/`: aggregates, SVG charts, manifest and review-verification JSON.
  `outputs/` is Git-ignored. The executed notebook and small review files can be shared
  with teammates; carry the supplied disclaimer with derived data shared externally.

## Verified baseline as of 2026-11-14

These are previously measured results, not assumptions to force onto future data:

- R1: participants equal visible BIC **occurrences**, excluding `...`, on all 10M
  rows. Distinct-visible-BIC counting differs on 59,191 rows with repeated BICs.
- R1b: all 767,204 N paths contain gaps; none of 9,232,796 Y paths do. Counting
  placeholders as participants explains that participant-count diagnostic exactly.
- Endpoint discrepancies are separate: ungapped Y paths include 460,440 sender and
  461,111 receiver mismatches. Groups can overlap. This does not prove bad data.
- A0: six nonblank labels total 7,006 rows. CUSTOMER_RECALL occurs 317 times and is
  not defined by the appendix; its mechanism remains unresolved. Blank: 9,992,994.
- UTC span: 2023-04-30 11:22:26 to 2023-07-31 09:56:01. April is partial and sparse.
  Monthly and pre-July/July checks were retrospective, not untouched holdouts.
- Timing/party/FX tables are descriptive baselines. No reviewed amount, duration,
  currency-choice, recurrence, text-pattern or anomaly-history mechanism yet.

Do not infer hidden banks or complete route length from participant count. Do not
claim that gaps explain all diagnostics. Do not infer recall behaviour from its name.

## Continue within the requested scope

Check `AGENTS.md` for current priorities. Possible next tasks are endpoint examples,
FX distributions conditional on routing/continuity/participants, amount quantiles by
currency and party pair, or UTC timing conditional on corridor and customer type.
Choose a bounded question and perform its independent review before expanding.
Account-pair and anomaly mechanisms require strictly preceding payment histories.
Human feature owners, deck editor and submission owner were unassigned at initial EDA.
Do not invent names or treat skill use as authority to submit files.
