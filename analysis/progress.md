# Initial EDA evidence record · 2026-11-14

Scope: starting-point reconciliation and first routing EDA. Full-file counts below
come from independent scans of all 10,000,000 retained cleaned records. No record
was removed, imputed or deduplicated. Economic theories remain hypotheses.

## Starting points

- Appendix pp. 3–4 checked directly against supplied case brief. Duration is seconds;
  B/C mean business/consumer; USD amount is normalized; tokens derive from detail text.
  `...` denotes a gap, not a visible institution. The original profile's contradictory
  limitation is historical and preserved; corrections are in the EDA manifest.
- Label census: blank 9,992,994; ROMANCE_SCAM 2,476; FAT_FINGER_MISTAKE 1,940;
  ACCOUNT_REPLACEMENT_SCAM 649; CEO_SCAM 945; DUPLICATE_PAYMENT 679;
  CUSTOMER_RECALL 317. Total nonblank 7,006 (0.07006%). The appendix lists five
  nonblank labels; it does not define recall. Blank means no recorded anomaly label.
- Historical routing diagnostics cover 1,665,936 rows, a different population from
  labeled anomalies. Flags are retained unchanged. No claim that all are invalid.

## R1 · Participant count follows visible occurrences

**Final wording:** In this supplied file, `participant_count` equals the number of
visible eight-character alphanumeric BIC entries in `bic8_path`, excluding literal
`...` placeholders, in **10,000,000 / 10,000,000 payments**. This applies within
every continuity flag × routing type. It is an exact observed encoding relationship,
not proof of the hidden generator's program or causal ordering.

| Continuity | Route | Rows | Count equals visible entries | Repeated visible BIC rows |
|---|---|---:|---:|---:|
| N | Covered | 51,262 | 51,262 | 1,827 |
| N | Direct | 315,266 | 315,266 | 0 |
| N | Indirect | 400,676 | 400,676 | 8,176 |
| Y | Covered | 364,700 | 364,700 | 9,566 |
| Y | Direct | 6,008,014 | 6,008,014 | 6 |
| Y | Indirect | 2,860,082 | 2,860,082 | 39,616 |

Initial A conclusion: exact visible-entry equality, zero unknown tokens; repeated
BICs make unique-institution interpretation fail. Initial B conclusion: independently
the same exact equality; explicitly tested distinct-count, gap and endpoint alternatives.
Neither agent saw the other's initial result. See each `reviews/*/initial.md`.

Strongest challenge: perhaps participants count distinct institutions, or include hidden
institutions. Deciding comparison: the **59,191** repeated-BIC records still match
occurrence count and fail distinct count; all gapped paths also match visible count.
This rules out those proposed universal count definitions for the observed field.
The file cannot disclose how many institutions a gap hides.

Self-consistency: all three independently generated joint route-count tables agree
exactly (PASS in `verify_reviews.py`). A monthly comparison matches 6,161 April rows,
3,044,400 May rows, 4,050,160 June rows, and 2,899,279 July rows. B independently
splits before/after July 1 UTC. Equality persists throughout. April is partial/small;
these are retrospective stability checks, not an untouched predictive holdout.
No sampling confidence interval is needed for this exact full-file census; future
or unobserved populations remain outside its scope.

Possible business interpretation: reported participants track observed route positions.
Repeated positions need not mean distinct institutions; hidden banks cannot be recovered
from this count. This is primarily field semantics supporting later economic analysis.
No FX-step or duration mechanism is inferred yet.

Calculation references: lead blocks 2/4/5; `review_a.py`; `review_b.py`;
`outputs/eda_initial/route_counts.csv`, `route_month.csv`, `route_summary.csv`,
`review_verification.json`. Chart: **R1_visible_participants.svg**. Source-record examples:
`route_examples.csv` (first encountered examples, not representative).

## R1b · Gaps explain the token-count diagnostic, with limits

**Final wording:** In this file, literal gap presence agrees exactly with continuity N:
**767,204 / 767,204 N** paths have gaps; **0 / 9,232,796 Y** paths do. Counting
all semicolon tokens as participants adds the placeholders and produces precisely the
767,204 existing `path_participant_count_mismatch` diagnostics. No unknown non-BIC,
non-gap entries were observed. Some paths contain multiple placeholders (up to six).

Both initial reviews found exact flag/gap alignment, stable by route type and period.
Strongest challenge from B: endpoint disagreement may be a separate process.
Deciding comparison: endpoint flags by continuity × route type. Among ungapped Y
paths, sender-endpoint mismatches total **460,440** and receiver-endpoint mismatches
total **461,111**. Therefore gaps cannot explain all routing diagnostics. These are
separate counts that can overlap; do not add them to infer unique affected rows.

Lead verification compares B's independently recomputed endpoint mismatches with the
preserved cleaning flags by stratum, as well as A/B/lead gap counts. Both debate
responses accept this narrower conclusion (`reviews/a/debate.md`, `reviews/b/debate.md`).
Endpoint substitutions, synthetic route construction, or field-definition nuances remain
possible explanations; this pass does not distinguish them. Do not call them corruption.

Evidence: `route_diagnostics.csv`, B `joint_counts.csv`, `review_verification.json`.
Gap presence alone does not locate or count the hidden banks. This result shares
R1's feature group and review; it is not a separate final dashboard in this pass.

## A0 · Label coverage, no inferred anomaly mechanism

**Final wording:** The supplied file contains six recorded nonblank anomaly labels;
CUSTOMER_RECALL accounts for 317 / 10,000,000 records (0.00317%) and has no definition
in the supplied appendix. Both independent full-file censuses and the lead census
reconcile every label exactly with the historical profile, including blank.

Strongest challenge: do recall or blank labels imply specific payment behaviour?
No: neither counts nor absence from the appendix establish a mechanism or legitimacy.
Deciding calculation is exact label-code reconciliation; recall-history testing remains
open. Self-consistency covers independent counts on the same full population; no label
mechanism is claimed that could be validated over time. Economic theory of a customer
reversal is untested and must not appear as a finding.

Evidence: `labels.csv`, both initial/debate records, `review_verification.json`.
Chart **A0_label_counts.svg** includes nonblank counts and states the blank denominator.

## Other saved EDA controls and remaining work

`party_pairs.csv`, `time_composition.csv` and `routing_fx.csv` are descriptive starting
tables, not reviewed generator rules. Numeric range/mean controls are in notebook
block 3; heavy-tailed amounts require conditional quantiles before interpreting typical
payment sizes. Question/theory register: [questions.md](questions.md).

Next: humans assign feature owners, deck editor and submission owner. Review source
record examples for endpoint mismatch; then choose conditional FX, amount or timing
tests. Historical account-pair/anomaly work needs time-sorted prior-only features.
All future material insights need the same independent review procedure. Final PDF
production and submission are intentionally outside this initial-EDA scope.
