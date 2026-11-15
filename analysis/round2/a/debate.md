# Reviewer A response after exchange

## Amounts

B's currency-conditional log shifts and C's USD-only quantiles independently support
the approximately exp(2) business-role scale shift. A's full blank-label table reproduces
their aggregate medians; exact cell comparison should be performed by the lead.
Strongest challenge is currency/bank mixture, not measurement precision. Currency-only
conditioning disproves currency mix as the entire explanation but does not separate
bank-pair and customer composition. Wording should remain a stochastic scale rule,
not an exact dollar multiplier or proof of a lognormal generator.

The `ALL` sentinel collision was a real reporting bug, not a data anomaly: eight real
currency ALL cells and eight synthetic totals were mixed by the filter. Old table/log
were preserved; corrected script uses `__ALL_CURRENCIES__` and reran from the complete
cache. This did not affect the original computed quantiles or group assignments.

## Duration and FX

B's low July R-squared for linear route/participant/FX models agrees with A's huge
within-cell duration spread and rejects a comprehensive deterministic additive-delay
formula. It does not reject a smaller stochastic stage effect. A additionally fit
single exponential, single lognormal and two-lognormal mixtures on pre-July exact
continuous route/participant histograms, scoring all July rows. Direct p2 NLL improves
7.495925→6.827667→6.447098 and total variation .577931→.393964→.132463.
The two-component model also improves Indirect p3/p4 and Covered p3, but its residual
error is appreciable. A mixture is useful reconstruction, not uniquely identified
generator code. Bank-conditioned models or sums of bank-stage mixtures remain plausible.
This deeper fitted model needs B's independent review before being called verified.

A's zero FX>country-change exceptions on continuous paths and cross-country FX0
cases challenge a naive conversion-per-country-border rule. Internally inferred
currency groups are a promising next test; avoid importing a real-world currency map.
Without testing complete path sequences against those groups, do not claim a complete
FX rule. Marginal FX0 and FX1 duration differences cannot establish an FX-caused delay.

## Route length and gaps

B's negative-binomial comparison addresses A's strongest objection: p2 can contain
multiple gaps, which a single Bernoulli insertion per visible edge cannot generate.
Both fits agree around q=.05, and B's July model discrepancy strongly favors geometric
insertions per visible edge over binomial gaps or using p rather than p−1 opportunities.
Keep observational equivalence explicit: neither direct geometric sampling nor flooring
an exponential variate is uniquely identified. Route-length and gap mechanisms are
candidate distributions, not recovered source code or counts of hidden banks.

## Label restrictions and histories

All A/B/C label-party censuses agree: CEO implies business sender; romance implies
consumer sender but not consumer recipient. These are constraints, not sufficient
evidence of an injected fraud mechanism.

The strict-past same-pair/currency exact-repeat result agrees independently: 493/679
duplicates match an earlier amount; 515 have observed history. The latest exact-prior
lags supplied by C distinguish rapid replays from arbitrary recurrence, but selected
unlabelled controls are conditioned on label-bearing pairs and are not population controls.
Missing history means unrecovered, not necessarily inconsistent with the label.

The initial fat-finger discrepancy (A0 vs C3) came from tolerance units. A originally
allowed ±one predecessor cent when dividing; C allows ±one resulting target cent.
Correct integer arithmetic is abs(prior−target×factor)<=factor for division. After
that correction, A gives FAT3 and controls548, matching C. Preserved old logs and
corrected row outputs show the deciding comparison. No tolerance: FAT0 and controls83.
Thus exact universal power-of-ten replay is unsupported; the negative result is robust.

A still finds3 romance power matches versus C's1 because A tries every exponent±1..6,
while C selects one nearest log-ratio exponent. Near tiny target amounts, tolerance
can admit more than one power even when the nearest candidate fails. This is a
definition difference, not evidence of a romance decimal-shift mechanism. Lead should
choose a shared definition or report both sensitivity results. Exact-power counts are0.

Account replacement has0/649 same-pair history; recall59/317 with no repeats; CEO2/945.
These constrain what same-pair history can explain, not whether other histories contain
the original transfer. Broader sender history is the right deciding next comparison.

## Text-country token alignment

Lead/B and A independently agree exactly on present/missing counts and comparisons:
all6,084,595 present ordering country tokens match orderingbank code; only59,826 of
6,107,358 present beneficiary country tokens match beneficiarybank code, and88,333
match orderingbank. Missing is separate on both sides. Strongest alternative is
token-derived formatting/coverage rather than real customer residence. These counts
describe encoded field alignment; they do not identify where customers live or prove
recipient banks were assigned randomly. Period/type strata are the deciding stability
comparison and are saved in A's full text joint table.

## FX graph deciding comparisons

Lead/B's allDirect zeroFX equivalence graph agrees with A independent6,323,280/6,323,280
Direct fit. A then freezes preJulyDirect graph:9,999,964/10M route predictions match;
36 overpredictions by1, no unknown countrycodes. Only14 exceptions occur in July.
This temporal result retains sparse failures instead of claiming perfect prediction.

Train with ALLDirect, exclude ALLNonDirect from graphlearning, and predict the latter:
3,676,707/3,676,720 nonDirect rows match,13 overpredictions remain. This fixes23 of
the previous36, including the four JulyDirect links (LC–GD, KN–GD, AI–LC, WF–NC).
The remaining13 involve FM–US orMP–US transitions, with no directly observed zeroFX
supporting those mergers. These are plausible sparse-link gaps, not proven arbitrary
exceptions or countrycurrency facts imported from outside the dataset. Candidate
additional mergers need an early-data constraint test and later validation.

The requested all-data constraint follow-up shows necessity/sufficiency within this
candidate family: FM–US-only leaves5 errors; MP–US-only leaves8; both leaves0/10M.
The model with both link discoveries predicts FX as visible country-zone transitions
on every supplied row. This refines a deterministic observed encoding rule, but its
last13 residuals were used for discovery, so it has no untouched validation for the
refined rare links. Independent B assessment of whether the residual constraints
uniquely require those links remains a separate review step.

Both gap-free and gapped paths are tested separately. Near-equality on gap-collapsed
visible routes is compatible with placeholders not contributing independent FX steps.
It does not uniquely establish whether the generator computed FX before or after
inserting placeholders. The final rule should say "inferred currency-zone transitions
explain almost all FX counts" with exact exception counts, not "country borders cause FX".

## Romance recurrence mechanism

After A's blind calculation, C independently reports lag mean307/SD301seconds and
log amount-ratio mean.403/SD.410. These agree with A's phase-stratified estimates:
early lagmean313.55,SD310.41; July292.69,SD279.87; logratio mean.4014/.4033,
populationSD.4087/.4099 (sampleSD is slightly larger, which must be reconciled).
An exponential interarrival scale≈300sec and lognormal multiplier with logmean/logSD
≈.4/.4 fit both moments and quantiles. July medianlag212sec, medianratio1.4886 remain
near early217sec and1.5. This supports a stochastic burst-and-escalation rule on the
1973 recoverable samepair/currency romance histories. Only5 ratios are exactly1.5.

Strongest objection is historyselection:503 labels have no observed history and a
previous legitimate payment can differ from the source event the generator modified.
Sameparty/period selectedcontrols still have much longer lagmedians and ratio medians
near1, but are not population-matched causal controls. Future refinement should score
fitted distribution likelihoods on July and inspect source-record chains, rather than
claiming that every labelled payment follows a fixed schedule or amount factor.
