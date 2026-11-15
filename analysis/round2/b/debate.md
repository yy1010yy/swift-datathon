# Reviewer B debate and boundaries

This follows saved independent initial.md,history_initial.md,history_lag_initial.md,
token_initial.md and fx_initial.md. A/C/lead findings were exchanged only after the
corresponding B initial, except explicitly noted participant-length discussion below.

## Amount scale and heaping

A and C independently reproduce all-currency and USD role medians, and A's
currency-conditional log shifts agree with B's approximate exp(2) interpretation.
Strongest objection: currency and bank mixtures can mimic a universal factor, and
rounding affects median ratios. Deciding comparison is exact unlabeled currency×party×
period quantile reconciliation, then earlier-period fixed-currency log models evaluated
on July. B fitted sender-business factor7.15056 and receiver-business7.41106; interaction
adds little explanatory power. July log-amount R²=.30728 and residual logRMSE2.15035.
Thus use approximately sevenfold scales after currency adjustment, not an exact7.39
per-payment rule. A currency-mixture-only explanation is insufficient, but bank/corridor
and party selection remain. A broad common multiplicative noise family is plausible;
an exact lognormal source is not identified by logmean/logSD alone.

USD's integer-dollar heaping is reproduced by C. B contrasts38.636%USD with.935%EUR
on unlabeled full populations. Possible rounding-before-normalization mechanism is
plausible but not proven: only USD-normalized amounts are available. Stable heaping
by currency×party×period is in rounding_currency_party_period.csv. Avoid naming an
unobserved original-currency amount or exchange-rate function as recovered.

## Duration: negative linear result plus partial mixture model

A identifies very different fast/slow duration behavior and approximately200-second
mean increments among Indirect participant counts. B's full-census OLS result is
consistent: route/participant/FX linear models explain only2.20%of July variance.
The strongest challenge to a fixed FX surcharge is A's DirectFX1 mean belowFX0,
stable inJuly; do not turn that into causal acceleration from conversion.

A's earlier-fit two-lognormal model improves July distribution fit over single
exponential/lognormal: DirectP2 NLL6.447 versus6.828singlelognormal/7.496exponential;
totalvariation.13246 versus.39396/.57793. Other displayed route/count groups also
improve, but remainingTV.13–.17 is substantial. It is a better partial model, not an
exact recovered two-lognormal generator. Unmeasured bank processing, currencies,
and stage mixtures remain alternatives. Lead should compare exact group populations
and preserve both the improvement and model misfit.

## Gaps, route length and FX zones

A's gap proposal and B's independent initial agree on negative-binomial gap count
with r=visible participants−1 and failure probabilityapproximately.05. B's July
Pearson discrepancy27.76/47expected>=10cells versus9,128.49for same-rbinomial is
the deciding comparison. This makes multiple gaps possible on a single visible edge;
it does not identify hidden institution count or causal insertion direction.

The shifted-geometric participant distribution was described by A/lead before B
independently fit it; B's subsequent assessment is debate-stage confirmation, not
a blind initial. Do not misrepresent the review provenance for that separate rule.

B independently finds the same all-data DirectFX equivalence partition as lead/A:
6,323,280/6,323,280 agree. A's pre-July-trained graph produces rare one-step FX
overpredictions on JulyDirect and longer routes. This is the strongest challenge to
a perfectly recovered partition: sparse codes may lack early zeroFXlinks. Report
exact residual counts and their group/time populations; do not replace them with
the all-data discovery's perfect fit. B's inferred-currency alternative matches all
5,948,508known-codeDirects, but374,772are unscored due to missing same-country
training observations. Payment-currency-endpoint heuristic fails83,397known-code
rows, supporting currency-zone boundaries rather than payment currency alone.

Deciding residual check: B independently re-predicts the36shared exception records
using its own allDirect graph, leaving13errors. FM–USmerge leaves5,MP–USmerge leaves8,
bothleave0; no new errors arise among all6,323,280Direct counts. A's full10Mcache
rescan then shows bothmerges leave0errors anywhere. The concentration of same-sign
residuals on these missing links favors incomplete-zone constraints over scattered
random FX noise. However bothlinks were learned from exceptions, so final10Mexactfit
is refineddiscovery, not a freshvalidation. Earlier frozen-map36exceptions and excluded
route13exceptions must remain visible. Sparse unsupported code-pair equivalences
could admit more than one completezone assignment.

## Text geography

Lead and A reproduce B's raw-scan result: all6,084,595present ordering-country tokens
match ordering-bank country. Beneficiary match is only59,826/6,107,358present tokens.
The deterministic sender relationship therefore cannot be generalized to recipients.
Missing tokens are explicitly excluded from the match denominator, and allmonth/type
joint counts are saved. Corresponding token/raw-text alignment does not independently
prove genuine customer geography: tokens are derived features. Receiver-country/bank
association should not be called random independence without testing its marginals.

## Histories and labels

C and B exact-prior/history-eligibility counts agree on all22,523shared-extractrows.
For duplicate labels,493/515history-eligible payments repeat a prior amount; eligible
blank selected-pair controls209/14,788. This supports a replay mechanism for the
recoverable subset, with164duplicate labels lacking strict prior same-pair/currency.
Controls are selected by labeled pairs, not causally matched; account text variations
and observation boundaries can hide sources.

Fatfinger only3/313eligiblepower10matches versus548/14,788controls is an informative
negative result for this narrow history mechanism, not proof labels are wrong.
Recall and account replacement cannot be reconstructed from pair-only absence.

B's initial broad±1targetcentpower test gave3romance matches versus C1. Deciding
rows469714and2305660 involve$.01/$.02amounts: cent tolerance alone spuriously admits
arbitrarily tiny shifted values. Adding an independently implemented nearest-decade
ratio constraint reproduces C's one match and all other row indicators. Both original
and narrowed definitions are retained. Main duplicate/fatfinger conclusions unchanged.

CEO/romance sender-type constraints independently agree across A/B/C;665romance
business receivers refute a universal consumer-to-consumer restriction. Names alone
cannot identify economic intent.

## Romance recurrence/growth model

B independently confirms1973observed-prior romance rows, median215seconds, ratio
median1.5;1639increase323decrease11equal. Strict monotonic escalation is false.
Earlier-fit exponential waiting(mean313.55s) and normal loggrowth(mean.40138,SD.40868)
give July KS.03782/.02506on624rows. FixedExp300/Normal(.4,.4)also fits approximately;
CB/CCperiodchecks saved. Compare scores against lognormalwaiting/gammashape2 and
Laplace loggrowth in recurrence_model_scores.csv, not just model-shaped quantiles.

July waitingtimeNLL is6.68143for exponential versus6.83401gamma(shape2) and6.74480
lognormal. July normal-loggrowthNLL.52709beatsLaplace.57492. These are early-fit
candidate families compared on624later observations, preserving identical denominators.
The event clusters and retrospective exploration prevent treating descriptive KS
values as pristine iid hypothesis tests.

Matched-control limit: all2476romance rows lie in500exact accountpairs with no blank
payments in those same pairs. A within-pair labeled/blank causal comparison is therefore
unavailable. Pooled selected-pair controls differ in history depth and purpose. These
are stochastic injection candidates with finiteobservational support; no verified
customer psychology or exact simulator code is claimed. Source/timestamp tie choices
must match before comparing latest-prior ratios; equal timestamps never count as past.
