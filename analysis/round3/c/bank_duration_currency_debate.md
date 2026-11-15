# C response to B: bank/corridor, duration and alternative currency

C read B's initial only after both initials were saved. The two implementations use the
same supplied source but different raw caches and model forms.

## Population and unit reconciliation

B's currency/duration models use all records strictly before/after July1, including
the partial April30 and July31 boundaries:7,100,721 train and2,899,279 July rows.
C excludes both partial boundary dates:7,094,560 May–June and2,896,968 July1–30.
B's blank-label amount population is separately7,095,842/2,897,152. Timing uses the
same complete-date population as C. The near-identical duration baseline log RMSE
(B1.993864, C1.993851) and currency sender-country accuracy (both89.43%) show that
boundary rows do not drive the common conclusions.

B counts8,720 BICs across endpoints and visible paths; C's independently scanned endpoint
cache has8,686 ordering/beneficiary BICs. The 34-code difference is scope, not a raw-count
conflict: C did not encode path-only intermediaries. Currency is categorical accuracy/NLL;
duration scores natural-log seconds. These units must not be compared to round2 raw-second R².

## Bank/corridor evidence and strongest challenge

B's strongest new route result is exact-corridor Covered choice: among524 pairs with
at least100 non-Direct rows in each period, early/July rate correlation is.99984 and
89.31% of earlier rates are below1% or above99%. The July pair model reaches98.39%
classification accuracy on seen cells but only86.26% of rows have an earlier pair key.
C accepts this as evidence against a country-only route-choice rule. It is also consistent
with C's duration result that endpoint identities and pairs carry stable parameters.

The challenge is simulator coverage and causal level. A pure pair lookup has no rule for
13.74% of July non-Direct rows, and alpha changes NLL materially (.120 at10 versus.205
at100). The deciding comparison should therefore be a hierarchical earlier-fit model:
exact pair when adequately supported, sender BIC fallback, then sender country/global,
reported with coverage and NLL on one July population. If that preserves the pair gain,
final bounded wording is: **Covered versus Indirect is largely a stable exact-bank-corridor
preference for previously observed corridors, with sender-bank/country fallback; the data
do not reveal why the corridor has that preference.**

## Duration: C's additive model resolves B's separate-effect comparison

B fits one correction at a time after route×continuity×participant×FX: sender BIC log
RMSE1.5335, receiver1.6439, exact pair1.6053. C fits sender then receiver additively,
because both endpoint effects can coexist. On complete dates, that lowers RMSE to1.1890
and raises log-duration R² to.6609. UTC hour-of-week adds essentially nothing
(R².6612), while a smoothed pair residual reaches RMSE1.1096/R².7047. Thus B's
pair-alone score does not contradict C's residual pair gain; they condition on different
preceding components.

Temporal stability independently agrees. B sender-effect correlation is.99847 at
minimum100 and.99948 at1,000 rows each period. C obtains.99947 for1,105 sender BICs
and.99946 for925 receiver BICs at500, plus.98742 for2,448 residual pairs at100.
The decisive lead check should reproduce C's additive ordering on B's cache or reverse
the sender/receiver fitting order. A large gain under both orders distinguishes stable
two-endpoint parameters from a one-sided composition artifact.

Final bounded wording if verified: **log-duration location contains stable sender-bank
and receiver-bank components plus a smaller directed-corridor component after route,
participant and FX stages. These parameters explain about70% of later log-duration
variance, but not the residual fast/slow mixture or literal operational cause.** Exact
BIC may proxy a bank-correlated service class; prediction alone does not prove queues.

## Alternative currency: independent modal and probabilistic tests agree negatively

B's probability score is the strongest challenge to an exact-bank/corridor currency
story: sender-country NLL.54272 beats exact sender BIC.56883 and strongly beats exact
pair1.36149 at fixed alpha100. C's independent mode test reaches the same conclusion:
sender country89.43%, sender BIC89.42%, and thresholded pair modes never improve.
Thus the lack of exact-bank gain is not an artifact of choosing accuracy versus NLL.

C extends the result to the alternative cases. The sender-country top two currencies
cover94.80% and top three96.77% of July; among first-mode misses, the second accounts
for50.9% and third another18.6%. Receiver-country mode is correct43.90% on sender-BIC
misses, slightly below the global modal currency44.06%; receiver BIC is43.78%. Exact
pair modes are only1.79% correct on any previously seen pair and weaker for dense pairs.
The evidence therefore challenges a receiver/corridor override mechanism.

Final bounded wording: **currency is drawn from a stable sender-country-specific menu:
one dominant choice plus a small number of alternatives. Exact sender bank, receiver
bank and directed corridor do not add robust later-period prediction. The probability
weights for rare fourth-or-later choices remain unresolved.** A deciding lead comparison
should reconcile C top-k counts with B's sender-country probability table and report both
NLL and top-k coverage, rather than promoting a deterministic modal rule.

Evidence: C `initial.md`, `duration_model_scores.csv`, `duration_effect_stability.csv`,
`currency_model_scores.csv`, `alternative_currency_scores.csv`; B `initial.md`,
bank model and stability tables. All period splits are retrospective checks.
