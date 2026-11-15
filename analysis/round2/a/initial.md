# Reviewer A independent initial conclusions — round 2

Saved before seeing B/C results. All 10,000,000 cleaned records scanned in 261.5 s.
Scripts, exact tables and actual logs are beside this file. Numeric cache is ignored
`outputs/round2/a/numeric.npy`. No exclusions except blank-label base-amount comparisons.

## R2: country changes are an upper bound, not the FX rule

On all 9,232,796 continuous paths, FX never exceeds the number of adjacent visible
BIC-country-code changes. FX equals that count on 8,141,743, leaving 1,091,053
exceptions to equality. All direct same-country-code paths have zero conversions;
531,407 direct country-changing paths also have zero conversions. Largest examples
are FR→DE/EUR, DE→FR/EUR and other recurring cross-code pairs, and GB→IM/GBP.
No external currency map was used. Candidate mechanism: conversion follows currency
boundaries rather than every country boundary. Evidence supports rejection of the
country-change equality rule; a fully inferred currency-zone map remains untested.

Evidence: `routing_joint.csv`, `direct_country_currency.csv`; both preserve exact counts.
Country-like code is BIC positions 4:6. Gap-collapsed paths are excluded from transition
claims because adjacent visible banks may not be actual neighbors.

## D1: duration has a wide fast/slow mixture; no fixed FX surcharge identified

Continuous Direct paths all have two participants. Before July, FX0 has n=668,397,
mean 703.75 s and median45 s; FX1 has n=3,597,706, mean656.12 s and median38 s.
July reproduces the direction (698.78 vs655.66 s; medians44 vs38). Thus a universal
positive FX-delay increment is not supported by this conditional comparison. It does
not establish that conversion causes faster processing: currency/country/bank mix
is a competing explanation still needing adjustment.

Continuous Indirect duration means before July are845.07 s at p3,1047.09 s at p4,
1249.79 s at p5; July845.55,1044.75,1230.01. Median jumps89→411→591 s in early data.
The roughly200 s mean increment is a partial stochastic stage-delay rule, not a fixed
per-payment formula. Covered has different distributions even at p3 (early median288 s
vs Indirect89 s). Within-count route differences and bank/currency mix remain unresolved.
Gap status has very similar duration distributions at a given type/participant count.

Evidence: `duration_conditional.csv`, `duration_route_participants.csv`. Full empirical
histogram is saved under `outputs/round2/a/duration_histogram.csv`. Timing is seconds,
all rows retained. Pre-July/July is retrospective stability, not untouched validation.

## R3: endpoint mismatch process fits approximately5% per endpoint

Full joint totals: neither9,027,029; receiver-only474,572; sender-only473,706;
both24,693. Marginals sender498,399 and receiver499,265, approximately5% each.
Both near0.25% is compatible with independent endpoint changes, but does not identify
the editing process or prove routes incorrect. Need compare by month/type/continuity.

## R4/R5: candidate route-length and gap distributions

Explicit provenance: fitted to the prior full-file independent A route census, not a new
independent gap scan. Direct count is exactly2; non-direct count fits3+geometric failures
with success~0.632 (also consistent with floor exponential scale1). Gaps fit a sum of
geometric failures across p−1 positions, failure~0.05, not a binomial count of single
gaps: p2 paths can contain2+ consecutive placeholders. Exact fitted parameters and
expected/observed cells are `route_distribution_fit.csv` and `gap_model_cells.csv`.
Multiple programs can produce the same distributions; source code is unidentifiable.

## V1 and A1

Full amount calculations completed before seeing B/C findings. An initial reporting
bug used `ALL` as both the actual currency code and a synthetic grand-total label;
the original table/log are preserved with `before_sentinel_fix` names and corrected
script uses `__ALL_CURRENCIES__`. The corrected script is rerunning from cache.
Numerical conclusions here were independently calculated before exchange; this prose
appendix was written after the exchange arrived, so distinguish computation independence
from report-writing timing.

Blank-label early all-currency median USD amounts: BB22,880.23; BC3,115.24;
CB3,246.435; CC463.70. July22,891.96;3,123.47;3,211.515;463.44 respectively.
Within-currency mean log10 amount shift BB−BC has170 sufficiently populated cells
(both n>=500), mean0.867431, median0.869656, SD0.036265. BC−CC has132 cells,
mean0.868289. This is approximately multiplication by7.4 per business role,
consistent with an additive2-unit shift on natural-log amounts. Means/medians alone
do not identify the exact generating distribution; bank and corridor composition
remain alternative explanations for residual variation.

All945 CEO_SCAM rows have business senders. ROMANCE_SCAM has1811 CC and665 CB
rows: consumer sender is universal, consumer recipient is not. Thus a literal C→C
restriction from the appendix description is refuted by665/2476 observed rows.
Other labels cover all party pairs. Exact table: `label_party.csv`. This establishes
restrictions in this file, not how the historical fraud injections were implemented.
