# D blind initial: visible correspondent choice and Covered routing

Saved before reading B's round-3 intermediary or bank conclusions. Full raw scan kept
all 3,676,720 non-Direct rows. Models fit 2,611,021 pre-July rows and score 1,065,699
July rows. Literal gaps are excluded as banks; first/last refer only to visible BICs.

## Visible intermediary choice

The first visible intermediary's pre-July global distribution gives July top-1
accuracy 3.3135% and NLL 6.4897. Currency, sender-country+currency, exact sender-BIC+
currency and endpoint-pair models do not improve NLL; sparse endpoint-pair models are
worse and have only 80.45% known-key coverage (67.91% after FX stratification). The
same conclusion holds for the last visible intermediary. Sender-country+currency
raises top-1 first-intermediary accuracy only 0.063 percentage point while worsening
NLL, so it is not a useful recovered selection rule.

The global pool is temporally stable: pre-July versus July marginal total variation is
0.01743 first and 0.01799 last; rate correlations among BICs with at least 100 rows in
both periods are 0.99992 and 0.99989. The most common BIC has only about 3.3% share.

Initial conclusion: visible intermediaries are consistent with a stable, diffuse global
bank pool under the tested features, not a strongly endpoint/currency-specific preferred
pool. This is a negative conditional test, not proof of independent random sampling.
Unmeasured position, full path state, learned FX-zone component or another rule could
matter, and hidden banks behind gaps are unobservable.

## Covered versus Indirect

The route label is different. Earlier-fit July NLL falls from 0.352294 global to
0.325912 by sender country, 0.235804 by exact sender BIC, and 0.120369 by directed
endpoint-BIC pair. Known July endpoint-pair coverage is 86.26%. Thus Covered choice
contains strong stable exact-bank/corridor structure beyond country. Shrinkage changes
hard-classification accuracy for small cells, so NLL and coverage are the primary
comparison.

This predicts the encoded label but does not prove a business causal order. Exact bank
pairs could proxy a preassigned corridor class or another latent network attribute.

Evidence: `intermediary_review.py`, actual run log, `intermediary_models.csv`,
`covered_models.csv`, `intermediary_stability.py` and its executed outputs. The initial
attribute-access failure and cancelled inefficient anomaly scorers are preserved.
