# Independent A latent fat-finger model

Written before seeing C's results. `fat_latent_model.py` fits the baseline on all
7,095,842 pre-July blank-label payments using weighted meanlog amount by currency
and business sender/receiver indicators. Estimated business shifts are1.9672 and
2.0030 natural-log units. Currency residual SD comes from within-cell log variance
plus additive-model lack of fit. All1940 FAT labels have known currency baselines:
1351 early for fitting error weights,589 July for scoring. No historical predecessor
is required, so this tests a latent intended-amount explanation rather than repeats.

The base-amount-plus-decimal-shift hypothesis is a normal logamount baseline shifted
by k×ln10. EM fits weights over k=−3..3 or−6..6 on early FAT rows. Full logamount
density is scored on July, with lower mean negative loglikelihood better. Scores and
weights are saved exactly, together with every labeled/control residual.

Before adding competing broader-variance model: July unchanged baseline NLL5.9771,
single continuous shift4.4722, decimal mixture−3..3 2.9787, mixture−6..6 2.9591.
Thus simply calling them ordinary payments with one positive scale shift is inadequate.
The wide mixture locates mass near−2 and positive1..4 powers; neighboring positive
weights are unstable and heavily overlapping. No exact discrete choice weights recovered.

A deliberately stronger competing hypothesis allows arbitrary logamount location
and additional logvariance, fitted early. This tests whether broadened selection can
explain the same tails without an exact decimal-shift mechanism. Its final score is
in `fat_latent_scores.csv`; the comparison must accompany any decimal-error claim.
Also test a transparent equal-weight example at powers{−2,1,2,3,4}; this example
was chosen after inspecting initial mixture weights and is disclosed as exploratory.

Negative controls: deterministic every997th blank record (10,022 rows, not claimed
representative); other labels all retained. Blank early/july mean residual is−.0343/.0048
and logSD≈2.14/2.12, versus FAT3.55/3.72 and5.12/5.07. CEO has smaller positive
shift and greater spread; recall/replacement center near baseline. These strengthen
label-specific amount distortion, not proof that a given earlier payment was modified.

Limits: normal logbaseline is approximate and ignores amount heaping/bank mix. The
best-fit latent shifts do not identify intended counterfactual amounts. A broad or
multimodal selection process can mimic digit errors. Currency-only controls do not
establish causal direction. Historical samepair failures remain informative but do
not refute an error applied to a newly generated amount without a recorded precursor.
