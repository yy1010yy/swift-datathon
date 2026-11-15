# FAT latent model: A/C debate and narrow final wording

A's initial and C's initial were saved independently. Both fit the ordinary-payment
baseline before July using currency and business-sender/receiver terms. The lead's
`../fat_residual_verification.json` reconciles the1940 labelled residuals and both
baseline coefficient sets; differences in likelihood reflect model definitions,
not different target populations or amounts.

## Common result and deciding comparison

Both analyses use1351 pre-July FAT labels for fitting and589 July labels for scoring.
After currency/party adjustment, early residual mean/SD are3.5539/5.1174 and July
3.7249/5.0692, versus ordinary baseline log SD about2.15. The labelled amount
distribution is much wider and shifted upward; this repeats in July.

A uses a currency-specific residual SD, while C uses the single full-population
residual SD2.15062295. Consequently July unchanged-baseline negative log likelihoods
are5.9771(A) versus5.9626(C). The broad continuous mean-and-variance alternative
scores3.0429(A) versus3.0428(C); decimal-shift mixture scores approximately2.9787(A)
versus2.9779(C) for shifts up to three places, and2.9591(A, up to six) versus2.9587
(C, up to four). These close results support numerical/model consistency, not exact
equality of densities with different spread definitions.

## Strongest challenge: a flexible continuous distribution

The broad continuous alternative explains much of the improvement over ordinary
amounts. Decimal-shift mixtures improve July fit further, but their neighboring
components overlap substantially and fitted weights change with the allowed shifts.
Several C fits reach2000 iterations. Thus no unique shift set, mixing probability,
or row-level intended amount has been recovered. A multimodal nondecimal selection
process could imitate these distributions; approximate baseline lognormality, rounding,
bank mix and limited labelled counts remain boundaries.

A's blank-label negative control gives worse fit for the decimal mixture than for
the ordinary baseline. That supports label-specific distortion, while the deterministic
every997th blank control sample is not presented as a representative random sample.
C independently used full-population blank moment controls. The deciding comparison
retains both broad-continuous and decimal-mixture results, rather than comparing only
ordinary amounts to a more flexible mixture.

## Relationship to historical tests

The earlier same-pair exact-power search found no observed precursor for FAT labels.
That is compatible with errors applied to a newly generated intended amount whose
uncorrupted version is not a separate record. It does not establish that this is the
generator's actual operation. Same-sender exact-shift tests also show no enrichment
relative to matched earlier unlabelled controls; neither history search reconstructs
the intended amount.

## Final wording

FAT_FINGER_MISTAKE amounts have a much broader currency/party-adjusted distribution
than ordinary amounts. A candidate construction first draws an ordinary intended amount
and then shifts its decimal point by several places. This family predicts July labelled
amounts better than the unchanged baseline and slightly better than a broad continuous
normal alternative. The exact shift choices and probabilities remain unresolved; no
individual intended amount or causal source program is established.

Evidence: A/C `fat_latent_initial.md`, model scripts, actual logs, row-level residuals,
model-score tables, and the lead's residual verification. Claims about exact decimal
operators remain provisional; the adjusted broadening/upward shift is reproducible.
