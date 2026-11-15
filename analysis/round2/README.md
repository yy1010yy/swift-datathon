# Extended generator investigation

Read `../round2_methodology.md` for questions, rival explanations and review design.
Use `findings.md` as the canonical one-file report containing the findings,
explanations, challenges and evidence. `evidence_registry.md` is the compact status index.
The four targeted follow-up areas are reproducible under `../round3/` and have been
folded back into the same canonical findings file.
This directory holds compact, shareable scripts, actual run logs and result tables.
Large working arrays remain in ignored `outputs/round2/`; the cleaned data is unchanged.
Carry `../dataset_disclaimer.txt` with any derived artifacts shared outside the project.

## Executed analysis index

| Investigation | Code and actual stdout | Results / completion gate |
|---|---|---|
| A: routing, FX, endpoint mechanisms, durations, independent amounts | `a/analyze.py`, `a/summarize.py`, `a/run.log` | Inspect A manifest/initial report; unfinished scans are not findings. |
| B: independent amounts and duration; currency corridors and timing | `b/investigate.py`, `b/run.log` | Exact conditional tables and initial report; inspect full population reconciliation. |
| C: independent amounts, anomaly composition, preceding pair histories | `c/anomaly_amount.py`, `c/run.log` | Requires BOTH passes and strict earlier-timestamp checks. |
| Lead: text formatting and derived token families | `../text_round2.py`, `../../outputs/text_round2.log` | `text/patterns.csv`, `text/families.csv`, `text/manifest.json` only after all 10M rows. |
| Lead: route, Covered-choice, timing and endpoint deciding models | `lead_*.py`, matching `.log` files | JSON/CSV summaries beside the scripts; see the evidence registry for review status. |
| C: ordinary directed-pair population | `c/counterparty_population.py`, actual logs | 9,992,994 blank rows; independent B regrouping is the remaining review gate. |

Each analysis records the code run and its actual output rather than requiring a new
empty notebook. Read the independent initial reports before the later debate reports
to see which conclusions were reached independently. `evidence_registry.md` links every
rule to its review state; discovery results remain provisional until reviewed.

For long runs, logs and memory-mapped files can exist before a run finishes. Do not
infer full-population coverage from their existence. Input identities use original
cleaned-file path, size/mtime and profile controls unless the individual script states
a stronger content checksum. Earlier/July comparisons are retrospective validation.
