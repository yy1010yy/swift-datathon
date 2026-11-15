# Generator-rule evidence registry

This is the handoff index for the extended EDA. “Reviewed” means at least two
sub-agents supplied calculations or challenges, the population and units were
reconciled, and the lead recorded a deciding comparison. It does not mean the hidden
source program is uniquely identified.

| ID | Candidate rule or negative result | Status | Independent records | Deciding calculation and main boundary |
|---|---|---|---|---|
| V2 | Currency sets a baseline amount scale; business sender and receiver multiply the typical amount by about 7.15 and 7.41. | Reviewed | A/B/C amount initials and debates | `amount_verification.json`; 1,228 cells agree. Wide residual spread means this predicts a distribution, not each payment. |
| V3 | USD amounts have a separate whole-dollar heaping process (about 38–39%, versus about 1% for EUR). | Reviewed partial | B/C rounding tables; A amount review | `c/rounding_controlled.csv`; exact rounding probabilities for every currency remain unresolved. |
| R1 | Participant count equals visible BIC occurrences excluding `...`; gaps exactly match continuity N. | Reviewed exact | Initial A/B reviews | `outputs/eda_initial/review_verification.json`; distinct BIC count is not the field definition. |
| R2 | FX count is crossings between data-learned country-code currency zones. | Reviewed near-exact | A/B FX initials and debate | Earlier Direct graph predicts 9,999,964/10M; exception-fitted refinement reaches all rows but is not holdout evidence. |
| R4 | Participant count follows `2 + geometric failures`, success about 0.63228; Direct iff count is 2. | Reviewed | A/B unified route reviews | `route_type_model_summary.json`; geometric and floored-exponential samplers are observationally equivalent. |
| R5 | Gaps follow a sum of `P−1` geometric-failure counts with continuation about 0.05. | Reviewed | A/B gap models and debate | `lead_count_models.csv`; binomial alternatives have support violations. Hidden institutions are not recovered. |
| R6 | Each route endpoint has an approximately independent 5% chance of disagreeing with its separate bank field. | Reviewed | A/B endpoint debates | `endpoint_model_summary.json`; cannot identify which field was edited. |
| R7 | For non-Direct routes, Covered probability varies strongly by sender code; FX/party add smaller prediction gains. | Reviewed | A/B Covered reviews | July NLL 0.352294 constant versus 0.325958 fixed sender model. Bank/corridor causes nested in code remain possible. |
| D2 | Duration is multi-scale; a simple additive route/participant/FX formula is inadequate. | Reviewed negative; mixture provisional | A/B duration tables, A mixture | July linear R² 2.20%; two-lognormal family improves prediction but detailed mixture parameters lack a second blind fit. |
| C2 | Sender-code modal currency predicts 89.43% of July; either endpoint mode covers 94.07%. | Reviewed partial | B counts; C and lead prediction | `currency_mode_validation.csv`; alternative-currency and bank-pair rules remain unresolved. |
| T2 | A shared 168-hour profile with sender-code phase predicts timing better than pooled or party-only profiles. | Reviewed | A/B timing initials and debate; lead reproduction | `timing_phase_model.json`; phase is relative and cannot be called a timezone. |
| P2 | Ordinary pair recurrence is highly heterogeneous; homogeneous Poisson/geometric count and waiting models fail. | Reviewed negative/partial | C full scan; B independent full regrouping; lead recomputation | `counterparty_review/verification.json`; observation-window censoring prevents interpreting longer July gaps as slower behaviour. |
| A2 | 493 duplicate labels replay an exact earlier same-pair/currency amount. | Reviewed | A/B/C history scoring | `crosscheck_verification.json`; 493/515 eligible, 493/679 overall. Shared extraction is disclosed. |
| A3 | Romance labels form 2–8 payment episodes with roughly exponential short waits and random multiplicative growth. | Reviewed approximate | A/B/C episode and recurrence reviews | `fx_recurrence_verification.json`; tied timestamps change three predecessors, and 503 rows lack strict history. |
| A4 | Fat-finger amounts are consistent with latent power-of-ten shifts, but visible prior-transfer matching is negative. | Reviewed partial | A/C independent fits; A/C debate; B/C controls | `fat_residual_verification.json`; shift factors/weights and intended amounts are not identified. |
| A5 | Simple observed-prior invoice replacement and recall signatures are not enriched over selected controls. | Reviewed narrow negative | B/C sender controls and debate | `sender_control_verification.json`; latent invoices, unmatched purposes and the recall definition remain open. |
| X2 | Ordering detail country token always matches ordering-bank code when present; beneficiary token usually does not match its own bank. | Reviewed exact encoding | A/B raw checks plus lead census | 6,084,595/6,084,595 ordering matches; beneficiary 59,826/6,107,358. Full text grammar is unresolved. |
| X3 | Every account has a `_FAKE_` prefix; its suffix is rendered on the first detail line in about 94% of fields. | Reviewed partial encoding | A/B independent 10M scans and debate | Ordering 9,436,890 and beneficiary 9,390,618 matches. Omitted identifiers and multi-BIC beneficiary reuse disprove a universal immutable identity rule. |

The readable explanations, economic interpretations and full limits are in
[`findings.md`](findings.md). Scripts and actual stdout are indexed in
[`README.md`](README.md).
