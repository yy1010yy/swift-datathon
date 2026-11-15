# C independent initial latent fat-finger distribution test

Saved before seeing A's latent-shift result. Use C's separately scanned full-file
unlabelled currency/party log-moment model; fit before July, evaluate July. The
labelled input is C's own full-file extracted labelled.csv. No actual intended
counterfactual amount is assumed or observed.

The baseline residual log SD is2.1506. FAT residuals have early n1,351, mean3.5539,
SD5.1174; July n589, mean3.7249, SD5.0692. Thus after currency/party adjustment,
fat-finger amounts are shifted upward on average and much more dispersed, consistently
across periods. Same-pair absence of decimal matches does not contradict latent errors.

July mean log likelihoods: unchanged normal baseline -5.9626; a free mean/SD normal
fit on early FAT rows -3.0428; EM mixtures with baseline SD and component means at
integer multiples of ln10 improve to -2.9779 for shifts±1..±3 and -2.9587 for±1..±4.
The baseline is a poor distributional explanation; decimal-shift mixtures are plausible.
They are not uniquely identified: a broader continuous/other-mixture alternative has
not been ruled out, baseline lognormality is approximate, and amount rounding remains.

Several EM fits reach the2,000-iteration cap. Component weights vary greatly across
allowed shift sets; do not quote these weights as recovered generator probabilities.
The raw fit log, all candidates, iteration counts and exact per-row adjusted values
are retained (`fat_latent.json`, `fat_latent_comparison.csv`, `fat_residual_cases.csv`).
Primary robust result is increased adjusted dispersion/upward shift; exact decimal
operators and original amounts remain provisional pending independent review.
