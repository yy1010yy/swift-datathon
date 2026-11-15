# B review of independent A/C latent fat-finger results

Read A/C blind latent initials and lead fat_residual_verification.json after B's own
recorded-history negative tests. These are distinct questions: an injected decimal error
may modify a newly drawn intended amount, without a prior recorded transfer to match.

## Evidence that survives independent comparison

A and C independently fit currency/party amount baselines on7,095,842earlier blank
payments and center all1940fatfinger amounts. Lead matches all1940residuals to within
1.25e−13; earlier1351/later589denominators agree. FATresidual logSDapproximately5.1
versus ordinarybaseline2.15; residual meanapproximately3.55earlier/3.72July. The
upward shift and excessspread remain after currency/customerrole adjustment, unlike
the original unconditional mean comparison.

On July589rows, A's unchangedbaselineNLL5.9771 and singlelocationshift4.4722 are much
worse than the decimalshiftmixture2.9591. The important stronger alternative is a
continuous location **and additional variance**, NLL3.04286. Thus the mixture's advantage
over a fair broadcontinuousalternative is about.084nats/row, not the much larger gain
over an unchangedbaseline. C independently reproduces essentially the same comparison
(freeGaussianNLL3.0428,decimalmixture2.9587). A uses currencyspecificbaselineSD and C
pooledSD, so their density scores are not required to be numerically identical.

## Strongest remaining alternative

A different multimodal/heavy-tailed selection process could produce the same adjusted
amount distribution without literal decimal operators. An unconstrained mixture with
comparable complexity has not been ruled out; the decimalmixture has many weights,
while the broadGaussianhas only location/spread. Weight instability and EMiterationcaps
make exact shiftprobabilities particularly weak. The appealing equalweightpowers
{−2,1,2,3,4}example was selected after inspecting weights, so its July2.9555score cannot
be presented as a preregistered recoveredrule. Parameterfitting and modelsearch occurred
on the supplied population; July is a retrospective temporalcheck, not an untouched
confirmationexperiment.

## Final qualified wording

**Fat-finger labels mark a much wider and upward-shifted amount distribution after
currency and customer-role adjustment. A model that multiplies a latent intended
amount by powers of ten explains the later-period distribution substantially better
than ordinary amounts or one fixed scale change, and modestly better than a free
continuous shift/spread model. This supports decimal-like amount distortion as a
candidate mechanism; it does not recover the intended amounts, exact decimal shifts,
or their probabilities.**

Keep the negative historyfinding alongside it: same-sender/currency exactpower10
matches23/1788eligibleFATrows versus32/1723controls, so the evidence does not support
a general rule of altering an earlier **recorded** payment. A latent intended amount
and an observed historical payment are different comparison populations. No contradiction
should be hidden by replacing one claim with the other.

References:A/fat_latent_initial.md,A/fat_latent_scores.csv,C/fat_latent_initial.md,
lead fat_residual_verification.json,B/sender_initial.md and exactsendercontroltables.
