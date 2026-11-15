# Independent C initial conclusions

Written before seeing other round-2 reviewers' conclusions. Full first pass: all
10,000,000 retained rows, exact quantiles from stored numeric vectors, no subsampling.
History tests require the second full pass and are initially pending.

## V-C: party-type amount scaling

Within USD payments without a recorded anomaly label, medians are approximately
40,194 (B→B), 5,227 (B→C), 5,000 (C→B) and 695 (C→C) before July. July medians
are 40,308, 5,231, 5,000 and 695 respectively. This suggests each business endpoint
multiplies a baseline amount scale, with B→B roughly 58 times C→C in this currency.
Do not call that exact universal multiplier: medians are affected by rounding and
other conditioning variables, and causal direction is not identified by medians.

Log-amount standard deviations are about 2.15 in all eight USD party/period cells;
whole-dollar fractions are about 38–39%. A common broad multiplicative amount
distribution plus a rounding process is a candidate mechanism. Normality and the
exact rounding choices are not yet established. Full currency-specific tables,
counts, tail quantiles and log moments: `amount_quantiles.csv`.

Competing explanation: currency mix creates differences. USD-only comparisons
rule out currency mix as the entire explanation within USD. Need a comparison
across other currencies and conditional periods, and independent numerical agreement.

## A-C: label/party constraints and a counterexample

All 945 CEO_SCAM records have a business sender (683 B→C, 262 B→B).
All 2,476 ROMANCE_SCAM records have a consumer sender, but 665 have a business
recipient (1,811 C→C, 665 C→B). Thus a rule requiring both romance endpoints to be
consumers is contradicted by 665 observed records. This does not establish whether
the recipient is a fraudster, mule, invoice collector or mislabeled party.

Other labels occur in every party-pair category. Source: `label_party.csv`, full
population counts; missing or blank anomaly labels stay a separate category.

Strongest limitation: labels describe named cases, but party constraints alone do
not recover their injected changes. Strict-prior history comparisons remain necessary.

## A-C2: strictly preceding same-pair history

Second full scan completed; 22,523 records occur in the directed pairs of labelled
payments. Exact raw account strings and matching currency are required; equal-time
observations never count as earlier history.

- DUPLICATE_PAYMENT: 515/679 have observed earlier same-pair/currency history;
  493/515 of those (95.73%; 493/679 overall, 72.61%) repeat an earlier amount exactly.
  Latest exact-prior lags range 1–6,940 seconds, median 1,100 seconds. This supports
  accidental rapid replays for the recoverable subset, without explaining all labels.
- Selected-pair unlabelled controls: 14,788/15,517 have history, 209 exact prior
  matches (1.41% of history-eligible controls). Controls are selected by labelled
  account pairs and may differ in history depth and purpose, so this is descriptive.
- FAT_FINGER_MISTAKE: 313/1,940 have prior same-pair/currency history; only 3
  have a power-of-ten match (0.96% of eligible), versus 548/14,788 controls (3.71%).
  This comparison does not support the simple prior-transfer decimal-shift mechanism
  in the observed same-pair history. Most labels (1,627) lack such observed history.
- ACCOUNT_REPLACEMENT_SCAM: none of 649 has observed prior same-pair/currency
  history; this cannot distinguish a new beneficiary substitution from sparse history.
- CEO_SCAM: only 2/945 have same-pair/currency history; CUSTOMER_RECALL has
  59/317, with no exact/power-of-ten match. Neither mechanism is reconstructed here.
- ROMANCE_SCAM: 1,973/2,476 have same-pair/currency history, but only 12 exact
  amount repeats and one power-of-ten match. Recurrence is not generally fixed-amount.

Row-level evidence: `history_tests.csv`; aggregate controls and missing-history
denominators: `history_summary.csv`; month/party/history-depth tables: `history_strata.csv`.
`summary.log` captures actual outputs. A broader same-sender/different-beneficiary
test is running because pair-only histories cannot assess account replacement fully.

Implementation self-check: a second vectorized scorer reproduces primary count results.
The first scalar/vector comparison exposed a ratio-to-last tie choice on five rows
with multiple earlier payments at the latest prior timestamp. Both now select the
first source row at that timestamp; no primary repeat/power count was affected.
