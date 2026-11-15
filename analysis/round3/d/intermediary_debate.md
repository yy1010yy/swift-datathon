# D/B correspondent and Covered-choice debate

D saved its blind initial before reading B. Both independently scan all 10M source rows
and obtain 3,676,720 non-Direct payments, split 2,611,021 pre-July and1,065,699 July.

## Intermediary pool

Both obtain first-intermediary July top-1 accuracy 0.0331351 from the earlier global
pool, marginal TV 0.01743 and rate correlation 0.99992 among 919 well-populated BICs.
B reports top-ten share19.21%; D independently shows the last visible intermediary has
the same negative conditional result, TV0.01799 and correlation0.99989.

D's blind unsmoothed global NLL6.48969 initially differed from B's Jeffreys-smoothed
6.26509 because 355 July first-intermediary rows (0.0333%) use BICs unseen pre-July.
The post-exchange smoothing recheck gives6.26502 and documents the full discrepancy.
At robust smoothing B finds global NLL6.26509 better than currency6.31297, exact sender
BIC6.39476 or pair6.28016. D's separately implemented conditional models likewise show
no useful accuracy gain and severe sparse-pair coverage loss.

Final wording: **visible intermediaries are drawn from a highly unequal but temporally
stable global hub-propensity pool; tested endpoint, country, currency and route-label
conditions add at most weak information.** This does not prove independent draws at
every path position or describe banks hidden by gaps.

## Covered versus Indirect

D independently reproduces B's alpha10 July NLLs: global0.352294, sender country0.325912,
exact sender BIC0.235804 and exact endpoint pair0.120369, with pair coverage86.26%.
Hard accuracy differs slightly because D thresholds the shrunken probability while B
uses the unsmoothed within-cell mode; NLL and coverage are the reconciled measures. B's
rate-stability cells show near-deterministic, persistent corridor preferences.

Final wording: **Covered versus Indirect is largely an exact directed-bank-pair property,
with sender-bank and country fallbacks for unseen corridors.** This predicts the encoded
route label but cannot distinguish literal bank choice from a latent corridor class.

Evidence: B initial/models/stability; D initial, models, stability and smoothing recheck.
