# B response after reading C: bank/corridor, duration and currency

B's `initial.md` was saved first. C independently scanned exact BICs and implemented a
different hierarchical duration model; C's modal currency tests use complete May–June/
July dates, while B's currency/NLL models include the sparse partial boundary dates.

## Reconciliation

### Duration

The baseline reproduces despite the small population boundary: B scores 2,899,279 July
rows with log RMSE 1.99386; C scores 2,896,968 complete-date rows with 1.99385. Both
therefore start from the same weak route+participants+FX explanation.

B adds one shrunk exact-bank residual at a time: sender BIC RMSE 1.53349, receiver BIC
1.64386, pair alone1.60533. C's richer additive hierarchy combines both endpoints and
gets1.18897, then adds a pair residual to reach1.10963. These scores are not contradictory:
B's single-factor challenge shows each endpoint carries stable information, whereas C's
model demonstrates that the two endpoint effects are complementary and that a smaller
corridor effect remains. B early/July sender-effect correlations .99847/.99948 across
population thresholds agree with C's .99947 sender/.99946 receiver at n>=500. C pair
correlation .98742 provides the independent pair-stability check B lacked.

Strongest alternative: endpoint BICs proxy customer composition, corridor, service tier,
or an unobserved processing regime rather than literally causing time. Hour-of-week adds
almost nothing after BICs in C, challenging a simple queue-clock story. Large remaining
seconds error and log residuals prevent calling the hierarchy an exact SLA/delay sampler.

Recommended final rule: **duration location is generated primarily from stable sending-
and receiving-bank effects on the log scale, after route stages, plus a smaller exact-
corridor adjustment; the remaining fast/slow distribution is unresolved.**

Lead deciding check: on C's exact complete-date mask, independently reconstruct the
route baseline, additive sender+receiver BIC predictions and pair residual, then match
the five July scores and effect correlations. Report both log RMSE and seconds MAE so a
good relative fit is not mistaken for precise seconds prediction.

### Currency and alternatives

B's probabilistic result and C's modal result agree on direction. B all-July sender-
country model accuracy89.4275%, NLL .54272 at alpha100; exact sender BIC accuracy89.4195%
and worse NLL .56883. C complete-date values are89.4273% versus89.4176%. Directed pairs
do not improve either implementation after sparse fallback.

C adds the important menu interpretation: top two sender-country currencies cover94.80%
and top three96.77%. On sender-mode misses, receiver-country/BIC modes do not beat the
global fallback, and exact pair modes collapse with denser-cell requirements. B's NLL
sensitivity independently challenges overfitting: country pair only narrowly helps with
alpha10 and becomes worse with stronger shrinkage; exact pair is much worse.

Strongest alternative: a latent bank/corridor/customer-purpose variable could generate
both the sender-country menu and remaining choices while being too sparse for modal pair
tests. The observed evidence rejects a general exact-corridor override; it does not prove
the country code is the literal generator input or recover probabilities for rare fourth+
currencies.

Recommended final rule: **draw currency from a stable sender-country-specific ranked
distribution: the first choice accounts for89.43%, first two94.80%, first three96.77%;
exact bank or corridor does not improve later prediction.**

Lead deciding check: score one earlier-fitted sender-country categorical distribution on
the same complete-date July rows, reporting top1/top2/top3 and NLL, then compare exact
sender BIC and pair with a predeclared smoothing value. This reconciles C's menu coverage
with B's probability calibration.

## Bank/corridor boundary beyond C's scope

B independently finds exact sender BIC and especially exact BIC pair strongly predict
Covered versus Indirect, with pair-rate correlation .99984 for 524 cells having n>=100
in both periods. C did not test route-label choice, so this candidate has not yet received
the required second independent calculation. The lead should not promote it until A or D
recomputes exact-pair cells from an independent raw scan and checks unseen-pair fallback.
