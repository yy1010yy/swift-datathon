# Reviewer B independent initial conclusions

Written before receiving other reviewers' conclusions. Full cleaned population:
10,000,000 records, preserved without exclusions except explicitly stated controls.
All calculations use supplied payment fields; no external economic/country information.

## V2 · Amount scales are approximately multiplicative by customer role

On the 9,992,994 no-recorded-label controls, earlier-period USD medians are BB
22,880.23; BC 3,115.24; CB 3,246.435; CC 463.70. July medians are 22,891.96;
3,123.47; 3,211.515; 463.44. Log amount means are approximately 10,8,8,6 respectively,
with log SD near2.28. This suggests roughly a factor exp(2)=7.39 per business role,
rather than an additive dollar increment. Amounts overlap very widely; this is not a
deterministic rule for individual payments.

Currency-conditional comparison challenges the currency-mix explanation: among
currency-period cells with at least1,000 rows in both groups, median **log-mean shifts**
for BB/BC are2.00091 (74 early currencies) and2.00861 (48 July currencies);
CB/CC1.98013 (42 early) and1.99706 (20 July). Conditional exceptions and selection
remain: BB/CB shifts range1.460–2.531 early, and BC/CC1.517–2.498. Bank-pair and
country/currency effects have not been fully separated, so exp(2) is a candidate scale,
not a recovered exact formula. Nor is a lognormal generator proved by these summaries.

Evidence: amount_unlabeled_party_period.csv, amount_unlabeled_currency_party_period.csv,
amount_conditional_ratios.csv, amounts_unlabeled_run.log, summary_run.log.

## V3 · USD has strong round-number heaping

Among unlabeled USD payments,657,604/1,702,039 (38.6362%) have integer-dollar amounts;
264,596 are multiples of100 and193,826 multiples of1,000. EUR has29,896/3,197,037
(0.9351%) integer-dollar amounts; other major currencies mostly approximately1%.
USD's most frequent amounts include10,000 (35,590 rows),1,000 (32,551),5,000 (21,666),
100,000 (16,979),500 (15,492),100 (13,620),50,000 (13,110).

Candidate construction: rounded payment-currency amounts are subsequently expressed
in USD, retaining obvious rounding for USD but not other currencies. Alternative:
currency-dependent amount mixtures or repeated templates could give similar heaping.
Only USD-normalized amounts are supplied, so conversion order and original local
amounts cannot be identified from this evidence alone. Need controlled/independent review.
Evidence: rounding_currency_party_period.csv, frequent_amounts_currency.csv, rounding_run.log.

## D2 · Simple additive delay model is a weak explanation

Fit only pre-July dates; evaluate July2,899,279 rows. Route-only OLS explains1.3324%
of July duration variance, RMSE1,218.08seconds. Adding participants,FX,continuity and
route-by-participant interactions explains2.2014%, RMSE1,212.70seconds. Improvement
is small; mean absolute errors remain near898seconds. This rejects these linear
models as a comprehensive delay generator; it does not prove route/FX never affect
duration. Exact conditional duration spreads and quantiles saved for investigation of
mixture/threshold processes. Evidence: duration_models.json,duration_route_fx.csv.

## R3 · Gap counts fit per-visible-edge geometric insertions

Independent model selection from previously parser-verified full joint counts, including
zero-gap Y routes. Let r=visible participants−1 and K=number of literal gap placeholders.
The negative-binomial family P(K=k|r)=C(k+r−1,k)(1−q)^r q^k gives early fitted q=.0498872.
This is consistent with a geometric number of gaps per visible edge with approximately
5% probability of another gap. On July cells with expected count>=10, Pearson discrepancy
is27.76 across47 cells versus9,128.49 for the same-r binomial alternative; using r=visible
participants gives9,551.06 even for the negative-binomial family. Not a universal
significance test: sparse cells omitted and exploratory model selection disclosed.
This is a probabilistic candidate, not proof of insertion direction or hidden bank count.
Evidence: gap_models.py,gap_models_offset_*.csv,gaps_run.log.

## T2/C2 · Baselines, with unresolved composition and calendar effects

Full May1–June30 and July1–30 dates only. Exposure-corrected weekend/weekday daily-rate
ratios are approximately.307–.312 early and.330–.334 July across all party pairs.
This supports less weekend activity but the month difference and weekday asymmetry
need explanation before claiming a fixed weekend probability. No customer-local hours
are inferred from UTC. Country-code corridor currency shares and sender-country UTC
profiles are saved; individual bank-pair mix remains untested, so no exact currency
selection or time-of-day rule is claimed yet.

## Additional independent label census

Separate minimal-column full scan label_party.csv reconciles all10M rows. CEO_SCAM
occurs only on business senders (945/945); ROMANCE_SCAM only on consumer senders
(2,476/2,476), with665 business receivers and1,811 consumer receivers. These are
composition constraints, not sufficient evidence of scam-generating mechanisms.

## Method and execution correction

Full scan completed152.2seconds and cache contains all10M numeric rows. Original
postprocessing attempted uint8*5000 and failed; run.log preserves the failure. Cast
to int32 fixes it in investigate.py. resume_duration.py executes the corrected duration
suffix on the complete cache; duration_run.log records its actual success. Its manifest
elapsed_seconds is duration-postprocessing time, not full-scan runtime. Quantiles were
computed before the failure and independently extended with unlabeled_amounts.py.
The final original script is rerunnable end-to-end. Inputs/profile remain unchanged.
