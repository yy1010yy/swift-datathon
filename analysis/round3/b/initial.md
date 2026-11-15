# Round 3 B independent initial conclusions

Saved without reading A/C round-3 outputs. All prediction models fit pre-July records
and score July. Alpha 100 is the fixed primary shrinkage comparison; alpha 10/1000
sensitivities are saved. These are retrospective temporal checks, not untouched data.

## B1: exact banks and corridors

### Currency: exact bank identity adds no robust improvement over sender country

On 2,899,279 July rows, the primary sender-country model has NLL **0.54272** and
accuracy **89.43%**. Exact sender BIC is worse (NLL **0.56883**, accuracy 89.42%);
exact directed BIC pair is much worse after shrinkage (NLL 1.36149, 91.87% known-key
coverage). With weak alpha 10, country pair only narrowly improves country alone
(0.54270 vs 0.54352) while exact sender BIC remains worse. Therefore the earlier
country-level currency result is not hiding a stronger exact-bank rule. Alternative
currency selection remains unresolved.

### Covered versus Indirect: exact sender bank and bank pair are strong stable rules

Among 1,065,699 July non-Direct routes, global Covered/Indirect NLL is **0.35229**;
sender country 0.32596; exact sender BIC **0.24014**; and exact directed BIC pair
**0.20534** at alpha 100. The pair top-class accuracy is **98.39%** versus 88.72%
global, but only 86.26% of July rows have an earlier observed pair. The weak-shrinkage
pair score is 0.12037, showing strong near-determinism in seen corridors but also
retrospective smoothing sensitivity.

This is temporally stable, not merely rare-cell fit. Among 524 exact BIC pairs with at
least 100 non-Direct records in both periods, early/July Covered-rate correlation is
**0.99984**, July-weighted absolute change **0.00161**, and **89.31%** of early rates
are below 1% or above 99%. For 1,608 sender banks meeting the same threshold,
correlation is 0.99553. Candidate rule: the generator assigns a largely fixed route
label preference to an exact bank corridor, with sender-bank fallback for unseen pairs.
It does not prove a real bank chooses the route or identify the underlying network rule.

### Amount: ordering bank supplies a stable secondary scale adjustment

After an earlier-fitted currency×party baseline, July log-amount RMSE is **2.14975**.
Adding a shrunk sender-BIC residual lowers it to **2.05947** (4.20%); receiver BIC
barely helps (2.14393), and sparse exact pairs score 2.10739. Sender-bank relative
amount effects are stable: correlation 0.97751 across 2,622 banks with at least 100
rows in each period and 0.99635 across 638 banks with at least 1,000. The supported
rule is a sender-bank-specific amount scale on top of currency/customer roles, not an
exact corridor amount rule. Customer/purpose mix within bank remains an alternative.

### Duration: bank-specific processing scales dominate the simple route formula

After route×continuity×participant×FX baselines, July log-duration RMSE is **1.99386**.
Sender-BIC correction reduces it to **1.53349** (23.1%), receiver BIC to **1.64386**
(17.6%), and exact pair to 1.60533. Sender-bank residual duration effects have early/
July correlation **0.99847** for 2,623 banks with at least 100 rows each period and
0.99948 for 639 banks with at least 1,000. This supports stable bank-specific processing
time scales or service regimes. It does not distinguish literal bank processing from
bank-correlated corridors, schedules or customer mix.

### Timing: exact bank does not improve the country-phase rule

For 2,896,968 complete-date July rows, sender-country hour-of-week NLL is **4.88561**
at alpha 1000, exact sender BIC 4.90685 and exact BIC pair 5.00518; pooled is 5.02805.
Exact bank identity therefore does not add stable timing prediction to the country-level
schedule. This supports retaining the more parsimonious country-phase timing rule.

Evidence: `currency_bank_models.csv`, `covered_bank_models.csv`,
`continuous_bank_models.csv`, `timing_bank_models.csv`, `covered_stability.csv`,
`sender_effect_stability.csv`; code `scan.py`, `models.py`, `stability.py`.

## B2: entity, relationship and intermediary-network formation

### Entity activity is extremely unequal, but activity alone cannot explain repeats

On 9,992,994 blank-label payments, 390,725 observed senders have payment-count Gini
**0.8668** (median 3, maximum 75,773); 2,589,757 receivers have Gini **0.7146**
(median 1, maximum 53,336). Partner-degree Ginis are 0.8472 and 0.6651. Thus a small
number of highly active entities can create substantial apparent network concentration.

However, an independence benchmark using the observed sender and receiver activities,
Poisson counts and conditioning on a pair being observed predicts **168,249** repeated
pairs versus **628,578** actually observed: **3.736 times** as many repeats as the
activity-only benchmark. Party-specific actual/expected ratios are 3.55 BB, 3.52 BC,
5.59 CB and 5.55 CC. Activity and popularity are therefore insufficient by themselves;
the generator needs pair/corridor affinity, schedules or another relationship-level
component. The benchmark uses estimated margins and conditions on observed pairs, so
it is diagnostic rather than an exact configuration-model likelihood.

### Intermediaries look like stable global hubs, not endpoint-specific choices

Among all **3,676,720** non-Direct routes, first-visible-intermediary activity has Gini
**0.9339**; the top intermediary has 3.33% and the top ten have **19.21%** of rows.
The marginal distribution is highly stable: early/July total variation **0.01743**,
correlation **0.99992** among 919 BICs with at least 100 observations in each period,
and the same ten BICs form both periods' top ten. Only 11,792 first intermediaries equal
the listed sender and 13,899 equal the receiver.

Simple earlier-fitted identity models do not improve July choice prediction over the
global hub distribution. Global NLL is **6.26509**; at strong alpha 1000, exact BIC pair
is 6.28016, currency 6.31297, sender BIC 6.39476 and receiver BIC 6.39528. Indirect and
Covered intermediary distributions differ only modestly (TV 0.02675). Candidate rule:
draw intermediaries from a very unequal but stable hub-propensity pool, with at most
weak context adjustments. This conclusion covers the first visible intermediary only;
multi-step dependencies, hidden-gap positions and network feasibility remain untested.

Evidence: `bank_activity.json`, `first_intermediary_models.csv`,
`network_stability.json`, `activity_independence.json` and cells; code
`pair_activity.py`. Pair analysis shares C's earlier blank-label raw extraction but
independently aggregates exact strings and scores the benchmark.

## Strongest uncertainties for debate

1. Exact BIC/pair effects may proxy customer or corridor composition rather than enter
   the generator directly. A comparison controlling exact customer/account mix would
   help but becomes history-dependent and sparse.
2. The Covered pair model has excellent seen-pair prediction but 13.74% unseen July
   rows; a hierarchical sender-bank fallback is necessary for a usable simulator.
3. The activity-only recurrence calculation is not a full degree-preserving permutation
   or fitted configuration model. Its large miss supports relationship structure but
   does not quantify a unique affinity distribution.
4. First-visible-intermediary marginal stability does not prove independent sampling of
   all internal positions. Route chains may contain transition rules invisible to the
   one-position categorical comparison.
