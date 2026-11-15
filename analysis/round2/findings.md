# Reconstructing the payment generator: consolidated findings, challenges and evidence

This is the canonical one-file report for this EDA phase. It is not a claim that the hidden program is uniquely
identified. Results below come exclusively from supplied payments. Definitions come
from the supplied appendix. Exact field relationships, approximate generating models,
and unresolved tests are distinguished. Supporting scripts, logs and compact tables
remain linked for reproduction, but the findings, explanations, challenges and evidence
needed to understand the conclusions are consolidated here.

## Proposed construction, with limits

A useful candidate model now has several supported layers: draw highly unequal entity
activity and add a relationship/compatibility layer; choose currency from a sender-
country menu; draw a skewed amount scaled by currency, customer roles and sender bank;
draw route length, assign Covered/Indirect mainly from the endpoint-bank pair, sample
visible intermediaries from a global hub pool, count currency-zone crossings and insert
display gaps; draw duration around stable endpoint-bank and corridor locations; then
inject label-specific sequences or endpoint/amount changes. This is a proposed way to
reproduce observations, **not a recovered causal ordering**.
Different programs can produce the same observed distributions.

## Method used

All calculations use only the supplied payment records and appendix definitions. We
preserved all 10M rows, exact account text, repeated edges, labels and route gaps. For
probabilistic rules we normally fitted or inferred a rule before July and evaluated it
on July; these are retrospective stability checks, not untouched experimental holdouts.
Every promoted insight received at least two sub-agent calculations or challenges,
denominator/unit reconciliation, an exchanged objection, and a lead deciding check.
Shared extractions are named wherever independent scoring did not independently repeat
raw parsing. Exact field identities, approximate distribution models, causal candidates,
and unresolved negative results are kept separate.

## Eight headline finding groups

The detailed sections below contain every supporting and negative result. These eight
groups are the recommended stopping-point shortlist for the eventual dashboard/deck.

| Finding | Plain explanation | Main evidence | Strongest challenge / limit |
|---|---|---|---|
| 1. Amount construction | Currency supplies a baseline; business sender and receiver independently raise the typical USD amount by about 7.15× and 7.41×. Sending bank adds a smaller stable scale adjustment. | 9,992,994 blank rows; 1,228 A/B/C cells reconcile; sender-BIC adjustment lowers July log RMSE by 4.2%. | Residual amounts remain wide; bank effects can represent customer or purpose mix. |
| 2. Route size and display gaps | Participant count follows a geometric-length rule; Direct is exactly the two-participant case. Gaps are inserted by a separate repeated-failure process near 5% per opportunity. | All 10M rows; Direct rule has zero violations; negative-binomial gap model beats support-incompatible binomial alternatives. | Geometric and rounded-exponential samplers cannot be distinguished; gaps do not reveal hidden banks. |
| 3. FX and route labels | FX counts crossings between learned currency zones. For longer routes, Covered versus Indirect is largely a persistent exact directed-bank-pair property; visible intermediaries come from a stable global hub pool. | Earlier FX graph predicts 9,999,964/10M; Covered July NLL improves 0.352294→0.120369 for seen pairs; intermediary early/July correlation 0.99992. | Pair coverage is 86.26%; gaps hide unknown banks and hub draws may still have weak context rules. |
| 4. Endpoint perturbations and duration | Route endpoints show nearly independent 5% mismatches. Duration has stable multiplicative sender-bank, receiver-bank and corridor locations rather than a fixed per-bank delay. | Endpoint rates 4.984%/4.993%. Exact endpoint banks raise July log-duration R² from 0.046 to 0.661; pair residual reaches 0.705. | Field-edit direction and the remaining fast/slow duration mixture are unresolved. |
| 5. Currency and weekly timing | Currency is drawn from a sender-country ranked menu; timing follows a shared weekly shape shifted by sender country. Exact bank does not improve either rule. | Sender-country top-1/2/3 currency coverage is 89.43%/94.80%/96.77%; shared timing phase NLL 4.87493. | Rare fourth-or-later currency probabilities and the economic meaning of relative phases remain unresolved. |
| 6. Anomaly processes | Duplicate, romance and fat-finger labels use distinct mechanisms. Account replacement forces a new recipient account; CEO adds an almost always new recipient and elevated amount. | Replacement prior account 0/649; CEO prior account 2/945 and median 2.63× prior amount; independent C/D reconciliation. | Missing intended invoices prevent universal rules; no visible history or reversal reconstructs recall. |
| 7. Text and account encoding | Ordering country tokens mirror bank code. Every account is `_FAKE_`; about 94% copy its suffix into the first detail line. | Full census of 20M detail/account fields plus independent A/B scans. | Beneficiary tokens usually do not mirror their own bank; identifiers can be omitted, reused across BICs and paired with changing details. |
| 8. Counterparty recurrence | Entity activity is extremely unequal, but activity and popularity alone cannot generate the observed repeat relationships; an affinity, schedule or compatibility layer is required. | 9,992,994 blank rows; activity-only benchmark predicts 168,249 repeated pairs versus 628,578 observed (3.74×). | The extra layer may be pair affinity, schedules, corridor constraints or latent segments; the test does not choose one. |

## Business explanation for stakeholders

The interpretations below translate the reconstructed rules into banking and customer
behaviour. They are plausible explanations supported by the measured patterns, not
claims that the records describe actual customers or that a specific economic story
has been proved.

### 1. Payment value reflects who is paying, who is receiving and the currency used

The generator appears to treat customer type as a proxy for the economic purpose and
scale of a payment. Within the same currency, adding a business sender raises the typical
amount scale by about **7.15 times**, while adding a business receiver raises it by about
**7.41 times**. Because the effects are approximately separate, a business-to-business
payment can have a typical scale roughly 53 times that of a consumer-to-consumer payment
in the same currency, although individual payments still vary widely.

For stakeholders, this resembles a market in which company payments include supplier
invoices, payroll, settlement and treasury transfers, while consumer payments are more
often smaller purchases or personal transfers. The strong USD whole-dollar pattern
(about 38–39%, versus about 1% for EUR) also suggests that the generator includes
currency-specific payment conventions rather than merely converting one universal
amount distribution. This means amount-monitoring thresholds should be conditioned on
currency and both customer roles. A large consumer transfer and a similarly sized
business transfer should not automatically receive the same interpretation. The evidence
supports different amount scales; it does not reveal the actual payment purpose.

The sending bank supplies a smaller but stable secondary adjustment: after currency and
customer roles, a sender-BIC correction lowers July log-amount RMSE from 2.1498 to
2.0595, a 4.2% improvement. This can help bank-level threshold calibration, but it may
reflect the bank's customer or payment-purpose mix rather than a price rule set by the bank.

### 2. Most payment routes are intentionally short, while gaps represent observability

The route generator strongly favours short paths: **63.23%** of payments are Direct and
therefore contain exactly two visible banks. Longer routes become progressively less
common according to a simple geometric-length pattern. After a route is constructed,
display gaps appear to be inserted by a separate process with a continuation probability
near 5% per opportunity.

In business terms, this resembles correspondent banking. Institutions prefer a direct
relationship when one is available; otherwise one or more intermediaries connect the
sender and receiver. A displayed `...` should be understood as incomplete visibility,
not as one known additional institution. For operations, compliance and fee analysis,
route length can indicate likely intermediation, but gap count cannot safely be converted
into a count of hidden banks. The exact geometric sampler is not uniquely identified,
yet the separation between route construction and route display is strongly supported.

### 3. FX follows currency areas, while Covered routing reflects the sender's network

FX steps are best explained by movement between learned currency-zone groups, not by
every change in national bank code. This matches real payment economics: two countries
may use the same currency or operate within a shared settlement area, so crossing their
border need not require conversion. Conversely, crossing into a different currency area
creates an FX step. The earlier-data rule predicts **9,999,964 of 10,000,000** observed
FX counts before exception-based refinement.

For non-Direct routes, Covered versus Indirect is largely an exact directed-bank-pair
property. An earlier-fitted global probability has July negative log loss 0.3523;
sender country improves it to 0.3259, exact sender bank to 0.2358, and an earlier-seen
endpoint pair to 0.1204. Seen-pair coverage is 86.26%, so a practical generator still
needs sender-bank and country fallbacks. A plausible business reading is that a corridor's
correspondent and funding arrangement is established in advance rather than chosen anew
for every payment.

The actual visible intermediary is different: first and last intermediaries follow a
highly unequal but stable global hub pool. The top ten first intermediaries carry 19.21%
of non-Direct routes, yet endpoint, country and currency conditioning does not improve
robust July prediction over the global distribution. For stakeholders, route *type* is
corridor-specific, while the particular visible hub behaves more like a draw from a
shared correspondent pool. This conclusion does not describe banks hidden by gaps.

### 4. Endpoint inconsistencies look like a controlled data process; duration needs SLA segments

Each visible route endpoint disagrees with its separately listed bank field in about
**5%** of records, and the two disagreements occur almost independently. That regularity
is more consistent with a deliberate synthetic perturbation or separately generated
representation than with occasional uncontrolled data-entry mistakes. Stakeholders
should therefore retain and investigate these rows rather than automatically deleting
them as corrupt. The data cannot tell us whether the route endpoint or the separate bank
field was altered.

Processing duration is also not a simple “one more bank adds a fixed number of seconds”
rule. On the log scale, route, participant and FX controls explain only 4.6% of July
variation. Adding exact sender and receiver banks raises this to 66.1%; a smoothed
directed-pair residual reaches 70.5%. The effects are exceptionally stable between the
earlier period and July. Operationally, this resembles bank-specific processing regimes
or service classes with a smaller corridor effect. A stakeholder should build SLA and
capacity views around both endpoint banks and the corridor, while retaining a residual
fast/slow mixture for individual variation. Prediction does not prove literal queues,
cut-offs or causality, but it is far stronger than the earlier route-only explanation.

### 5. Currency and transaction timing are anchored to the sending institution

A sender-country code's most common currency predicts **89.43%** of July payments; its
top two earlier currencies cover **94.80%** and top three cover **96.77%**. Exact sender
bank and directed-pair modes do not improve this result, and receiver information does
not explain the remaining misses. The generator therefore looks like a stable ranked
currency menu attached to the sender country, rather than a home currency followed by
a bank-pair override. For treasury and liquidity stakeholders, most currency demand can
be planned from the sender market's first three choices; rare choices still need a tail
distribution rather than ad hoc corridor rules.

Payment timing follows a related pattern. One shared weekly activity shape, shifted to
a different phase for each sender code, predicts July better than one global UTC profile
or separate customer-type profiles. This is consistent with institutions operating on
different market clocks and weekly schedules. Capacity planning should therefore align
staffing and liquidity buffers to sender-specific activity windows rather than one global
peak. The phases are only relative patterns learned from the data; without external
timezone evidence they must not be labelled as local timezones or business hours. Exact
sender BIC makes the later-period timing score worse than the sender-country profile,
which supports keeping this mechanism at the country/market level.

### 6. Different anomaly labels require different detection logic

Duplicate payments have the clearest recoverable business mechanism. Among the 515
labelled duplicates with usable same-pair history, **493 (95.73%)** copy an exact earlier
amount. A practical control would therefore search recent payments for the same sender,
receiver, currency and amount, while recognising that missing history prevents a match
for some genuine duplicates.

Romance-labelled payments behave differently: they occur in short episodes, usually
minutes apart, and amounts generally grow by a random multiplier rather than repeating
exactly. This is consistent with escalating requests to the same recipient, so useful
detection features include recent sequence length, short inter-payment time and amount
growth. Fat-finger labels instead have an unusually wide amount distribution consistent
with decimal-place shifts applied to an unobserved intended amount. Their intended value
usually does not appear as an earlier payment, so history matching alone is inadequate.
These findings support label-specific controls rather than one generic anomaly score.
They do not recover every labelled event. `CUSTOMER_RECALL` receives a stricter
bidirectional negative test in A6 below; its underlying off-file event remains unresolved.

Two additional label rules are now visible. Every account-replacement target uses a
recipient account not previously paid by that sender/currency; only 49 of 649 retain a
previously seen recipient BIC, while the amount stays near the sender's ordinary median.
This is broader than simply changing an account at the same bank. CEO labels combine a
business sender with an almost always novel recipient (only 2 of 945 accounts previously
seen) and an elevated amount: among history-eligible rows the median is at the sender's
71st prior percentile and 2.63 times its prior median. Useful controls are therefore
payee novelty plus sender-relative amount, not a universal fixed threshold. Recall still
has no recoverable signature: only one target has a prior reverse-direction payment and
none repeats that reverse amount exactly, no more than selected controls.

### 7. Detail text is structured payment-message data, not an independent customer profile

The ordering-side country token, when present, always repeats the ordering bank's country
code. Likewise, every account value has a `_FAKE_` prefix, and about 94% of detail fields
copy the account suffix into their first line. These patterns indicate that much of the
text was constructed from other transaction fields. Treating each token as a separate
customer fact would therefore double-count the same information.

For data engineering, sanctions screening and entity resolution, the implication is to
preserve the raw message but identify which elements are derived. Exact account text is
not a guaranteed global customer key: some beneficiary account strings appear with
multiple BICs, some details omit the identifier, and detail text can change over time.
Matching systems should combine account, role, bank and context rather than assuming one
string always means one immutable customer. The beneficiary country-token asymmetry also
warns against treating a bank location as the beneficiary customer's residence.

### 8. Repeat-payment behaviour comes from a mixture of customer relationships

Most observed sender–receiver pairs appear only once, but a small group repeats hundreds
or even thousands of times. This combination of many one-off relationships and a very
long repeat tail cannot be produced well by one common repeat probability within each
business/consumer category. The generator must contain substantial heterogeneity.

A plausible business explanation is a mixture of occasional purchases, recurring bills,
supplier relationships, payroll-like flows, high-activity customers and popular
receivers. This matters for forecasting and monitoring: a repeated payment is normal for
some relationships but unusual for others. Models should learn relationship history and
sender/receiver activity rather than applying one party-type average. The current data
show that activity alone is insufficient: an activity-based independence benchmark
predicts 168,249 repeated pairs, compared with **628,578 observed**, a 3.74-fold excess.
Models therefore need an additional relationship, schedule, compatibility or latent-
segment layer. The test cannot choose among those explanations, and observation-window
effects still mean July's longer gaps must not be presented as slower customer behaviour.

## V2 · Customer types shift the scale of amounts

Plain meaning: business-related payments tend to be larger, even when we compare the
same currency. A business sender and a business recipient each contribute a separate
upward shift. There is still a very wide range of amounts within each group.

Candidate model, natural logarithms:

`log(USD amount) = currency-specific baseline + 1.96719 × sender_is_business + 2.00297 × receiver_is_business + noise`.

Fit on 7,095,842 blank-label payments before July, evaluate on 2,897,152 blank-label
July payments. Estimated multiplicative factors: **7.15056 sender**, **7.41106 receiver**.
July residual log SD/RMSE **2.15035**; July R² **0.30728**. These are fitted average
effects, not an exact multiplier for every payment. A universal currency-invariant
base amount is contradicted by the conditional quantiles.

Independent evidence: A/B/C each scanned all 10M records and derived quantiles on
the same blank-label population. All **1,228** currency×party×period cells agree.
B and C independently fit the coefficients/RMSE to numerical precision; their initial
tiny R² difference came from early-mean vs July-mean denominators, explicitly recorded.
A independently estimated comparable within-currency log shifts. Debate: `a/debate.md`,
`c/debate.md`, B initial/review records. Deciding tests: `verify_amounts.py`,
`b/amount_scale_models.json`, `c/amount_model.json` and their execution logs.

Challenge: a few labeled outliers or currency mix might cause the pattern. Excluding
labels and comparing within currencies preserves it; residual bank/corridor mixture
is not fully controlled. Approximate common log spread is consistent with multiplicative
variation but does not establish an exact lognormal generator. Rounding/heaping is
another component: USD has approximately 38–39% whole-dollar values versus roughly
1% in EUR, persisting across party types/periods (`c/rounding_controlled.csv`).
Possible business meaning: companies make larger invoice/payroll-like transfers than
individuals. The dataset does not identify payment purpose or prove that explanation.

Chart: [V2](charts/V2_amounts.svg). Exact tables: A/B/C amount files. Original ALL-code
sentinel bug and failed lead check retained; corrected grand totals use a unique marker.

## R4/R5 · Route lengths and gaps follow simple count distributions

Across all route labels, participant count is compatible with `P=2+K`, where
`Pr(K=k)=s(1-s)^k` and **s=0.63228**. Direct is exactly the `P=2` case: all
**6,323,280** Direct rows have two visible BIC entries, and no non-Direct row does.
Conditional on a non-Direct route, three entries are most common; each additional
entry is progressively less common.
A rounded exponential and a geometric sampler are observationally indistinguishable
here. This is a distributional model, not an exact prediction of each route length.

Gap counts fit a sum of `P−1` geometric-failure counts, continuation probability
**q≈0.05**. Before July pooled q=**0.0498872**. In plain terms, a display position can
receive another placeholder repeatedly; it is not limited to one gap. A binomial
model allowing at most one gap per edge has actual support violations. A/B fit explicit
alternatives; B's fixed earlier-fit July check strongly favors the negative-binomial
model over binomial and the alternative using P rather than P−1 positions.

Independent A/B gap initials, debate, `a/fit_routes.py`, `b/gap_models.py`, and lead
`lead_count_models.py` preserve expected/observed cells and temporal/subgroup fits.
These fits reuse the previously independently validated route census; they do not
constitute fresh independent raw parsing. Participant-length model received a
debate-stage recomputation after A's numerical result was shared; preserve this
blind-review limitation rather than treating it as a second blind initial.

Route label choice needs a separate rule. Among **3,676,720** non-Direct rows, 11.31%
are Covered overall. On 1,065,699 July rows, earlier-fitted negative log loss improves
from **0.352294** globally to **0.325912** for sender country, **0.235804** for exact
sender BIC and **0.120369** for an exact directed endpoint-BIC pair. Earlier pair history
covers 86.26% of July non-Direct rows; unseen pairs therefore require sender-bank and
country fallbacks. Among 524 pairs with at least 100 non-Direct rows in both periods,
Covered-rate correlation is **0.99984**, and 89.31% have earlier rates below 1% or above
99%. B and D independently reproduce the NLLs and coverage. Candidate mechanism: assign
a persistent Covered/Indirect preference to a bank corridor, with hierarchical fallback.
This predicts the encoded route label but does not prove that a real bank makes the
choice or reveal the latent corridor class. Round-3 evidence: `../round3/b/initial.md`,
`../round3/d/intermediary_debate.md`, `../round3/lead/remaining_verification.json`.
Chart: [B3](../round3/charts/B3_covered_corridor.svg).

Possible mechanism: build the visible route, then add optional display gaps. Hidden
bank counts cannot be inferred from placeholders; this model explains presentation.

## R2 · FX depends on learned country-code groups, not every country change

Country changes alone overcount FX: on continuous paths, equality fails on 1,091,053
rows. A better candidate groups internal BIC country codes that appear together on
zero-FX direct routes, then counts crossings between groups along a path. No external
country/currency map is used. These learned groups are evidence for shared currency
zones, not independently verified legal-tender definitions.

Lead/A/B independently derive a graph from all Direct zero-FX pairs and reproduce
**6,323,280 / 6,323,280 Direct** FX counts. This is discovery on those routes.
Freeze only earlier Direct data: **9,999,964 / 10,000,000** full-file predictions agree;
36 overpredict by one, including 14 July exceptions. Freeze all Direct data and test
non-Direct routes excluded from training: **3,676,707 / 3,676,720** agree. Thirteen
remaining sparse-code exceptions involve connections unsupported by direct zero-FX
examples. Merging FM and MP with the internally learned US component resolves all
13 and fits all 10 million rows. The lead independently scored the saved extracted
sequences and reconciled those results in `fx_recurrence_verification.json`. The
extraction is shared with A. This refinement uses the exceptions themselves; it is
a further discovery, not a fresh holdout. The earlier validation errors remain relevant.

Deciding calculations: `lead_fx_zones.py`, `b/fx_zones.py`,
`a/fx_zones_validate.py`, `a/fx_routes_crossvalidate.py`, corresponding logs/cells.
Initials: A initial + FX notes, B `b/fx_initial.md`; subsequent debate records separate
all-data fit from temporal/route-group tests. Adjacent visible entries across gaps
need special wording: agreement on gapped paths concerns the encoded visible sequence,
not proof of which banks were hidden. Economic interpretation: conversion is needed
when crossing currency zones rather than every national border.

## D2/D3 · Processing time has stable bank and corridor scales

Direct routes with the same participant count range from seconds to hours. The original
linear route/participant/FX model explains only **2.20%** of duration in seconds; on the
more appropriate log scale, route/participant/FX cells explain **4.64%** of July
variation. Extra FX steps therefore do not provide a universal fixed surcharge.

A fitted two-group lognormal mixture outperforms a single lognormal or exponential
for several route-length groups. Continuous Direct p=2 July mean negative log-likelihood:
two-group **6.4471**, single-lognormal **6.8277**, exponential **7.4959** (lower is better).
The mixture still has substantial residual mismatch (total variation≈0.1325).
It is an improved predictive family, **not an identified exact delay rule**.

A/B exact conditional duration quantiles/means/counts reconcile (`verify_crosschecks.py`).
Round-3 B/C models independently show that exact banks provide the missing location
rule. On 2,896,968 complete-date July rows, adding sender and receiver BIC effects raises
log-duration R² from **0.0464 to 0.6609** and lowers log RMSE from **1.9939 to 1.1890**.
A smoothed exact-pair residual reaches R² **0.7047** and RMSE **1.1096**, covering
2,661,260 July rows with earlier pair history. Effects are stable: early/July residual
correlations are 0.99947 sender, 0.99946 receiver and 0.98742 for well-populated pairs.
The lead reverse-order check yields R² 0.6651 receiver-first versus 0.6609 sender-first;
averaging orders gives 0.6687, so the result is not an arbitrary fitting-order artifact.

Candidate mechanism: route stages set a baseline, endpoint banks set multiplicative
processing-time locations, and the directed corridor adds a smaller adjustment; then a
broad or mixed residual is drawn. This is a predictive construction, not proof of queues,
cut-offs or SLAs. The earlier two-lognormal family remains a useful residual candidate,
but its exact components are not identified. Round-3 evidence:
`../round3/c/initial.md`, `../round3/b/bank_duration_currency_debate.md`,
`../round3/lead/duration_order_verification.json`, and
`../round3/lead/core_verification.json`.
Charts: [D2 residual-family comparison](charts/D2_duration_models.svg) and
[D3 bank/corridor model](../round3/charts/D3_duration.svg).

## A2 · Many labeled duplicates copy an earlier amount

Strictly preceding same sender, recipient and currency: **515/679** labeled duplicates
have usable prior history; **493** have an earlier exact amount. That is **95.73%** of
history-eligible duplicates and **72.61%** of all labeled duplicates. Blank records in
the selected label-bearing pairs: **209/14,788** history-eligible records match an earlier
amount (**1.41%**). This strongly supports a prior-copy mechanism for a subset.

The 164 duplicates without that history remain unexplained by this test. An earlier
transfer outside the file, different payer or another mechanism is possible. The
controls are selected pairs, not representative payments or a randomized comparison.
A/B independently scored C's extracted 22,523 raw history rows before seeing C's counts;
all prior-availability and exact-match counts reconcile across A/B/C. Shared extraction
is a limitation distinct from independent scoring. Exact support/deciding check:
`verify_crosschecks.py`; initial/debate records and history scripts in A/B/C folders.
Chart: [A2](charts/A2_duplicates.svg).

## A3 · Romance labels form rapid, usually growing payment sequences

For **1,973** labeled romance payments with strict earlier same-pair/currency history,
median wait is **215 seconds**, median amount ratio **1.5**, with **1,639 increases,
323 decreases and 11 equal amounts**. It is not a fixed 1.5× rule. Selected blank-pair
records have much longer median waits, but these are different pairs; there are no
blank rows in the romance pairs, so a within-pair label/control contrast is unavailable.

Candidate recurrence: roughly exponential waiting time with mean≈300 seconds, followed
by a random amount multiplier `exp(N(0.4,0.4²))`. A/B agree on every latest-predecessor
row under numeric source-record tie-breaking; earlier-fit parameters are approximately
313.55 seconds and log-ratio mean0.4014, SD0.4087. B July distribution checks are compatible
with this simple family, not proof of the source code. C initially used a different
equal-timestamp predecessor for three ratios: preserve and report that sensitivity.

The **503** rows without strict prior history cannot be assigned a multiplier by this
test. B and C independently found 500 directed pairs, each containing 2–8 labeled
payments in one currency; three extra first-timestamp rows arise from ties. Initial
A/B/C results and debate, latest-row tables,
distribution fits, period/party summaries are in their directories. This mechanism may
represent repeated escalating requests, but real-world intent cannot be observed here.

## A4 · Useful negative results and label limits

Same-pair exact powers-of-ten: **0/313** history-eligible fat-finger records, compared
with 83/14,788 selected blank controls. Allowing one cent **after** transformation gives
3 fat-finger matches; tiny amounts can produce spurious matches, so exact and tolerant
tests are kept separate. A/B/C initial discrepancies exposed inverse-tolerance and
nearest-exponent differences; correction/sensitivity files preserve them.

A separate distribution test gives a positive but qualified clue. After adjusting for
currency and party type, fat-finger amounts have much wider log-amount variation than
the blank-label baseline: approximately 5.1 versus 2.15. Two independent early-period
fits found that a mixture of power-of-ten shifts predicts July better than an unchanged
baseline, and also better than a freely widened normal distribution. The improvement
over the latter is modest, fitted mixture weights are unstable, and some fits reached
their iteration limit. These results support investigating decimal shifts applied to an
unobserved intended amount; they do not recover the original amount or exact shift
probabilities. See `a/fat_latent_initial.md` and `c/fat_latent_initial.md`. A formal
same-input check matches all 1,940 adjusted residuals to within 1.3×10⁻¹³
(`fat_residual_verification.json`); A uses currency-specific baseline spread and C a
pooled spread, so their initial likelihoods are not identical. The A/C debate reconciles
the difference: on identical residuals and spread, likelihoods agree to 8.9×10⁻¹⁶.
Against a freely widened normal, the decimal mixture gains about **0.084 nats/row** on
July—supporting a discrete-shift family without identifying its powers or weights.
An unchanged model wins on a blank-label negative-control sample. See
`a/fat_latent_debate.md` for final wording and limits.

Broader sender histories recover prior activity for 1,788/1,940 fat-finger and 603/649
replacement labels, but simple exact-prior transformation tests show no enrichment
in C's selected-control comparison: fat-finger exact-power 23/1,788 vs 32/1,723 controls;
replacement different-recipient exact amount 8/603 vs 12/591 controls. These are
**narrow negative tests**, not general refutations. B independently scores all 11,615
target/control rows and agrees with C on every numerator and denominator
(`sender_control_verification.json`, `b/sender_debate.md`, `c/sender_debate.md`).
They do not refute the documented intended anomaly meanings: intended amounts/invoices
may be unobserved or defined differently. Round 3 resolves account replacement through
recipient novelty rather than prior-amount copying; recall remains a reviewed negative result.

Full label/party census independently agrees: all 945 CEO labels have business senders;
all 2,476 romance labels have consumer senders, but **665 have business recipients**.
An exact consumer→consumer romance restriction therefore fails in this file.

## A6 · Replacement and CEO force novel recipients; recall remains unobserved

C and D independently score all **649 account-replacement**, **945 CEO** and **317
CUSTOMER_RECALL** rows with strictly earlier exact sender/currency histories and selected
blank-label controls. Both implementations agree on every headline denominator and
value; D independently rescans the raw file and additionally retains reverse-direction
account histories.

For account replacement, **0/649** target recipient accounts have appeared previously
for that sender/currency, compared with **90/603** controls. History exists for 603
targets. Only **49/649** retain a previously seen beneficiary BIC, so the rule is not
simply “change the account at the same bank.” Target amounts remain ordinary relative
to sender history: median 1.012× the prior median versus 1.004× controls. Candidate
rule: generate or force a new recipient endpoint while leaving amount scale unchanged.

CEO labels combine three features: every sender is a business; only **2/945** recipient
accounts and **62/945** recipient BICs were previously used; and among 822 history-
eligible targets the median amount is at the **71.17th** prior percentile and **2.626×**
the sender's prior median. Controls are at the 51.70th percentile and 1.121×. Candidate
rule: choose a business sender, introduce an almost always novel recipient and draw an
elevated—but not fixed—amount.

Recall remains a reviewed negative result. Targets closely match controls on prior
account/BIC reuse, amount percentile and lag. D's bidirectional scan finds one target
with a prior reverse-direction payment versus two controls, and **zero** exact reverse-
amount matches. No visible prior-payment rule reconstructs the label; it may depend on
an absent request, status or post-payment event. Controls are not randomized or purpose-
matched, but their shallower histories would bias toward *more* target novelty, not the
opposite. Evidence: `../round3/c/initial.md`, `../round3/d/anomaly_debate.md`, and
`../round3/lead/remaining_verification.json`.
Chart: [A6](../round3/charts/A6_recipient_novelty.svg).

## X2 · Text country tokens have asymmetric alignment

Ordering country token appears in **6,084,595** fields and matches the ordering-bank
country code in every one. Beneficiary token appears in **6,107,358** fields, but matches
its own bank country in only **59,826**. Missing-token fields have their own denominator.
Do not assume customer country equals bank country on the beneficiary side.

Lead full text census covers 20M fields. A/B independently parse raw token/bank columns
on all 10M transactions and agree on exact counts, including month/type strata; no
multiple-country-token fields observed. Debate/evidence: text initial records and scripts,
lead `../text_round2.py` and `text/summarize.py`. Chart: [X2](charts/X2_country_tokens.svg).
This is an encoding relationship; international banking or independent field generation
are possibilities, not established explanations. Token families derive from raw text
and are not separate independent economic evidence. Full formatting census saved;
an exact text-generation grammar is unresolved.

## X3 · Fake account identifiers are usually copied into the first detail line

Every ordering and beneficiary account in all 10M records begins with `_FAKE_`. After
removing that prefix, the exact remaining identifier appears in the first detail line,
preceded only by one or more `/` characters, in **9,436,890 ordering** and **9,390,618
beneficiary** fields. Those are also the exact counts where it appears anywhere in the
detail text: when the identifier is present, it is placed on the first line rather than
elsewhere. The rule is common but not universal—563,110 ordering and 609,382 beneficiary
details omit the exact identifier. Counterexamples include bank-only and name/address
formats. All 20M account fields still retain the `_FAKE_` prefix.

A and B independently reproduce the full-file format counts with different parsing
implementations. They also challenge the tempting assumption that the string is a
globally unique, immutable customer-bank key. A's exact census finds 391,132 distinct
ordering accounts, each observed with one ordering BIC, but 61,606 of 2,590,877 distinct
beneficiary accounts occur with multiple beneficiary BICs; 61,690 account strings have
multiple BICs when both roles are combined. B's deterministic 3/256 account sample
independently finds 731 account/BIC conflicts and 8,500 accounts whose full detail text
changes, while no selected account changes B/C party type. Thus the supported construction
is a fake identifier plus an optional first-line rendering rule, not a proof of stable
real-world identity. Evidence: `a/account_construction.py`, `a/account_initial.log`,
`a/account_reuse_summary.json`, `b/account_details.py`, `b/account_initial.md` and logs.

## C2/C3 · Currency is drawn from a sender-country ranked menu

Fit earlier currency frequencies by sender-country code and evaluate complete-date July.
The first choice matches **2,590,679/2,896,968 = 89.43%**; the top two choices cover
**94.80%**, and the top three **96.77%**. Among first-choice misses, the second choice
explains about 50.9% and the third another 18.6%.

B/C independent implementations agree that exact bank and corridor modes do **not**
improve the country menu: exact sender-BIC accuracy is 89.42%, and thresholded pair
modes are equal or worse after fallback. Receiver-country mode explains 43.90% of
sender-mode misses, slightly below the global alternative mode at 44.06%; exact receiver
BIC and pair modes do not help. Candidate mechanism: draw currency from a stable ranked
distribution attached to sender country, rather than a deterministic home currency plus
receiver/corridor override. Exact probabilities for rare fourth-or-later choices remain
unresolved. Round-3 evidence: `../round3/b/initial.md`, `../round3/c/initial.md`, and
`../round3/lead/core_verification.json`.
Chart: [C3](../round3/charts/C3_currency_menu.svg).

## T2 · A common weekly schedule is shifted by sender code

On **2,896,968** complete-date July rows, an earlier-fitted pooled 168-hour UTC profile
has negative log loss **5.01885**. A separate sender-code profile improves this to about
**4.8765**. A compact model—one common weekly template with a circular phase for each
sender code—scores **4.87493**, slightly better than unrestricted sender-code profiles.
Party-type splits do not improve later-period prediction after sender code. A and B
independently reach the same result; the lead reproduces B's score.

Round-3 exact-bank checks strengthen the boundary: sender-country hour-of-week NLL is
**4.88561**, whereas exact sender BIC is worse at **4.90685** and directed BIC pair at
5.00518. The timing phase therefore belongs at the country/market-code level in the
current evidence, not at individual bank or corridor level.

Plain meaning: payment activity follows a weekly rhythm whose clock position differs by
ordering-bank code. The phases are relative rotations, **not identified timezones or
local business hours**. Currency, corridor or bank composition may mediate the result.
The 9,991,528 rows in 13 complete UTC weeks have nearly separable weekly volume and
weekday composition (total variation **0.00296**), but individual cells differ by up to
about 10%. Weekly totals cluster near multiples of 50,000; this possible quota mechanism
was noticed after inspection and remains exploratory. Evidence: `a/timing_extension_debate.md`,
`b/timing_debate.md`, `lead_timing_phase_model.py` and timing manifests.

## R6 · Route endpoints receive approximately independent 5% discrepancies

Across all 10M rows, the first visible BIC differs from the separately listed sending
bank in **4.98399%** of rows; the last visible BIC differs from the receiving bank in
**4.99265%**. Both occur in 24,693 rows versus 24,883.3 expected from the marginal rates
under independence. Earlier-fitted independent Bernoulli rates predict July's four joint
endpoint cells with weighted conditional total variation **0.000383**. A/B independently
reproduce the counts and stability across route/continuity strata.

Candidate construction: perturb each endpoint independently with about 5% probability.
The observations cannot identify whether the path or separate bank field was changed.
A redraw that selects the original bank would also make the observed mismatch rate lower
than the actual edit chance. Continuous paths contain discrepancies, so gaps are not
their sole source. Evidence: `a/endpoint_debate.md`, `b/endpoint_debate.md`,
`endpoint_model_summary.json`.

## P2 · Ordinary counterparty recurrence is strongly heterogeneous

The 9,992,994 blank-label payments form **8,258,480** exact directed account pairs.
There are **1,734,514** rows with a strictly earlier same-pair payment and eight later
rows tied at their pair's first timestamp. Most pairs occur once, yet the tail reaches
936 BB, 2,310 BC, 488 CB and 475 CC payments per pair. For BB, 92.05% of observed pairs
are singletons, while a positive-geometric model matched to its observed mean predicts
81.92%. Zero-truncated Poisson and geometric count families fail similarly in every
party group, ruling out one homogeneous repeat rate within party type.

Observed repetition is more common for business-sender pairs (BB 7.95%, BC 8.48%)
than consumer-sender pairs (CB 4.91%, CC 5.28%), but this is not yet a causal customer-
type effect: sender activity, receiver popularity, corridor mix and durable pair affinity
are competing explanations. July median observed gaps are longer than early-period gaps,
but censoring and changing cohorts make a slowdown interpretation invalid. The supported
partial rule is that the generator needs strong entity/pair heterogeneity rather than one
party-type waiting/count distribution. C's full scan and model cells are under
`c/counterparty_*` and `b/counterparty_*`. B independently regroups all 32 shared raw
partitions, matches every count/history denominator and reproduces the model failures.
The shared extraction is disclosed; the grouping and strict-prior joins are independent.
The final B/C debate therefore promotes this as a reviewed negative/partial result, not
a recovered exact recurrence sampler.

Round-3 A/B tests separate endpoint activity from relationship structure. Sender activity
is extremely unequal (Gini **0.8668**, median 3, maximum 75,773 blank-label payments),
as is receiver activity (Gini **0.7146**). Activity almost determines observed degree,
but it does not explain repeated pairs. B's full activity-independence benchmark predicts
**168,249** repeated pairs versus **628,578** observed, a **3.736×** excess. A's distinct
implementation and deterministic receiver sample finds observed/expected ratios from
3.36× to 7.31× across party groups. Thus a generator needs heterogeneous activity plus
another layer—pair affinity, recurring schedules, corridor compatibility or latent
segments. The data do not uniquely select that layer. Evidence: `../round3/a/entity_network_initial.md`,
`../round3/b/entity_network_debate.md`, and `../round3/lead/core_verification.json`.
Chart: [N2](../round3/charts/N3_pair_recurrence.svg).

## N3 · Visible intermediaries come from a stable global hub pool

Across all **3,676,720** non-Direct routes, first-intermediary activity has Gini
**0.9339**; the top BIC carries 3.33% and the top ten 19.21%. Early/July first-position
distributions have total variation **0.01743** and correlation **0.99992** among 919
well-populated BICs. D independently obtains 0.01799 and 0.99989 for the last visible
intermediary. The same first-position top ten persist across periods.

Earlier-fitted endpoint, country, currency and route-context models do not improve
robust July prediction over the global pool. After reconciling smoothing for 355 unseen
July BICs, B/D global negative log loss agrees at about **6.265**; conditioned models
are equal or worse and exact pairs lose coverage. Candidate mechanism: sample visible
intermediaries from a highly unequal, stable global hub-propensity distribution, with at
most weak context adjustments. This does not prove independent draws at all path positions,
model transitions between multiple intermediaries or reveal banks hidden by gaps.
Evidence: `../round3/b/initial.md`, `../round3/d/intermediary_debate.md`, and
`../round3/lead/remaining_verification.json`.

## Remaining boundaries

The residual duration mixture, rare fourth-or-later currency probabilities, full text
grammar, exact relationship-affinity process and CUSTOMER_RECALL mechanism remain unresolved. Full historical
invoice matching beyond visible transfers is not possible from these tests. A fully
specified simulator also needs bank/corridor/entity-population rules that the observations
do not uniquely identify. These are supported partial or negative results, not gaps to
fill with guesses. Human interpretation and final deliverable selection remain future work.
