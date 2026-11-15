# Extended EDA: questions, theories and analytical process

User expanded scope after initial EDA: reconstruct as much of the supplied generator
as possible, valuing demonstrated partial/negative results. All comparisons use only
supplied data. No GDP, real-country populations, local-time-zone lookup or external
currency mapping is introduced. BIC country substrings are internal code features.

## Investigation design

- **Routing / FX / duration (A and B independently):** Does FX count follow route
  length or observed country transitions? Does duration obey an additive formula or
  a route-specific distribution? Compare conditional support, residuals and strata;
  alternative: a mixture of route types creates an apparent participant effect.
  Where possible fit earlier dates and evaluate July; this dataset has already been
  explored, so period splits are retrospective checks, not pristine holdouts.
- **Values (A/B/C independently):** Does party type or currency set the typical
  log-amount or shape of the distribution? Compare conditional medians/quantiles and
  log distributions. Alternative: currency, route composition or labeled injected
  outliers create the pooled effect. Means alone cannot establish a scale rule.
- **Currency / timing (A/B independent; lead confirmation complete):** Does bank
  corridor explain currency choice? Do hour/weekday profiles persist within party
  and corridor, accounting for observed exposure? Alternative: changing corridor mix.
  UTC peaks cannot automatically be described as local business hours.
- **Anomalies / histories (C discovery; A/B independent scoring and debate complete):** Are labeled duplicates
  exact copies of strictly earlier transfers on the same directed account pair?
  Do fat-finger payments match earlier amounts times powers of ten? Does recall
  match earlier transfers? Compare unlabeled controls and distinguish no prior history
  from tested failures. A matching predecessor does not independently prove fraud.
- **Text / tokens (lead census; A/B country-token review complete):** Which formatting and token-family
  frequencies depend on party type? Do token country codes match the bank country
  substring? Are literal backslash-n and actual newlines distinguishable? Count each
  token family once per field, distinguish fields from transactions, check months.
  Alternative: tokens simply re-express deterministic formatting, with no separate
  business mechanism. Bank country and customer country can legitimately differ.
- **Counterparties (C discovery; B independent regrouping pending):** Does one
  party-type-specific count or waiting distribution explain repeated directed pairs?
  Compare exact pair counts, tails and strictly earlier gaps. Alternative: sender and
  receiver activity, corridor mix, durable affinity and observation-window censoring.
- **Account/detail construction (A/B independent full scans in progress):** Is the
  account identifier copied into the first party-detail line, and is reuse consistent
  across rows? Preserve exact strings and separately test formatting, BIC and label
  exceptions rather than normalizing identifiers.

## Evidence and execution records

Each agent owns its directory beneath `analysis/round2/`, including scripts, actual
execution logs, exact tables, initial conclusions and limitations. Do not edit each
other's initial results before exchanging them. The lead's text scan is
`analysis/text_round2.py`, log `outputs/text_round2.log`, aggregates `analysis/round2/text/`.
There is no claim of completion until the full scan reconciles to 10M rows.

Each candidate needs two independent subagent reviews, exchanged objections, a deciding
calculation verified by the lead, matching population/units/results, a stability test
where feasible, and separate final wording. Shared cached aggregates must be disclosed
as shared inputs; agreement on them does not independently validate raw parsing.

Final causal language is conditional: propose an explicit generative order or mechanism,
list its predictions and test counterexamples. Observational fit cannot uniquely recover
the program or establish economic intent. Report what the strongest alternative still
explains, and mark incomplete reviews or unresolved mechanisms provisional.
