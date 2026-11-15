# Reconstructing the payment generator: consolidated findings, challenges and evidence

This is the canonical one-file report for this EDA phase. It is not a claim that the hidden program is uniquely
identified. Results below come exclusively from supplied payments. Definitions come
from the supplied appendix. Exact field relationships, approximate generating models,
and unresolved tests are distinguished. Supporting scripts, logs and compact tables
remain linked for reproduction, but the findings, explanations, challenges and evidence
needed to understand the conclusions are consolidated here.

## Proposed construction, with limits

A useful candidate model has several parts: choose customer types and a currency;
draw a strongly skewed amount whose scale depends on those choices; construct a bank
route and count currency-zone crossings; insert gaps in the displayed route; draw a
variable processing time; add some special payment sequences or anomalies. This is
a proposed way to reproduce observations, **not a recovered causal ordering**.
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
| 1. Amount construction | Currency supplies a baseline; business sender and receiver independently raise the typical USD amount by about 7.15× and 7.41×. USD also has a strong whole-dollar rounding process. | 9,992,994 blank rows; 1,228 A/B/C cells reconcile; July log-model R² 0.307. | Residual amounts remain extremely wide; purpose, bank and corridor mix are unobserved. |
| 2. Route size and display gaps | Participant count follows a geometric-length rule; Direct is exactly the two-participant case. Gaps are inserted by a separate repeated-failure process near 5% per opportunity. | All 10M rows; Direct rule has zero violations; negative-binomial gap model beats support-incompatible binomial alternatives. | Geometric and rounded-exponential samplers cannot be distinguished; gaps do not reveal hidden banks. |
| 3. FX and route labels | FX counts crossings between learned currency-zone groups. For longer routes, Covered versus Indirect uses a stable sender-code-specific probability with smaller FX/party adjustments. | Earlier Direct graph predicts 9,999,964/10M FX counts; Covered July NLL improves 0.352294→0.325958. | Final FX exceptions were used to refine the graph; sender code can proxy bank/corridor mechanisms. |
| 4. Endpoint perturbations and duration | Route endpoints show nearly independent 5% mismatches with separate bank fields. Processing time is multi-scale, not a fixed additive delay. | Endpoint rates 4.984%/4.993%; July joint-cell TV 0.000383. Simple duration model July R² 2.20%. | Data cannot identify which endpoint field was edited; exact duration mixture remains unresolved. |
| 5. Currency and weekly timing | Sender code strongly predicts currency. Timing follows a shared weekly shape shifted by sender code rather than one global or party-only clock. | Sender modal currency predicts 89.43% of July; shared phase model NLL 4.87493 versus pooled 5.01885. | Alternative currency choices are unresolved; relative phases are not proven timezones or local hours. |
| 6. Anomaly processes | Many duplicates replay an earlier amount; romance episodes recur quickly with usually growing random multipliers; fat-finger amounts support latent decimal shifts. | 493/515 history-eligible duplicates exact-match; 1,973 romance predecessors; A/C fat residuals reconcile to 1.3×10⁻¹³. | Missing history and unobserved intended amounts prevent universal rules; recall remains open. |
| 7. Text and account encoding | Ordering country tokens mirror bank code. Every account is `_FAKE_`; about 94% copy its suffix into the first detail line. | Full census of 20M detail/account fields plus independent A/B scans. | Beneficiary tokens usually do not mirror their own bank; identifiers can be omitted, reused across BICs and paired with changing details. |
| 8. Counterparty recurrence | Ordinary repeated pairs require strong heterogeneity; one party-type Poisson/geometric count or exponential wait model fails. | 9,992,994 blank rows, 8,258,480 pairs, 1,734,514 strict-prior rows; B/C and lead verification pass. | Censoring, activity, popularity, corridor mix and pair affinity cannot yet be separated. |

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

For non-Direct routes, Covered versus Indirect is also not one universal random choice.
The probability varies materially and very consistently by sending-bank country code;
adding FX and customer type improves prediction further. A plausible business reading is
that different sending markets rely on different correspondent networks and funding
arrangements. Some routinely use reimbursement or cover chains, while others use serial
intermediation. This can inform route-cost and liquidity analysis: the relevant drivers
are the currency area and the sender's network, not nationality alone. Sender code may,
however, be standing in for particular banks or corridors, so the causal level remains
unresolved.

### 4. Endpoint inconsistencies look like a controlled data process; duration needs SLA segments

Each visible route endpoint disagrees with its separately listed bank field in about
**5%** of records, and the two disagreements occur almost independently. That regularity
is more consistent with a deliberate synthetic perturbation or separately generated
representation than with occasional uncontrolled data-entry mistakes. Stakeholders
should therefore retain and investigate these rows rather than automatically deleting
them as corrupt. The data cannot tell us whether the route endpoint or the separate bank
field was altered.

Processing duration is also not a simple “one more bank adds a fixed number of seconds”
rule. Route, participant and FX counts explain only **2.20%** of July duration variation,
and even otherwise similar Direct payments range from seconds to hours. Operationally,
this resembles multiple service modes or processing states—such as straight-through
processing, review queues, cut-off windows or bank-specific handling. A stakeholder
should segment service-level analysis by processing regime and corridor instead of
promising one universal duration increment. The data support multiple time scales but
do not identify the exact operational stages.

### 5. Currency and transaction timing are anchored to the sending institution

A sending-bank code's usual currency predicts **89.43%** of July payments; considering
the usual currency at either endpoint covers **94.07%**. This suggests that customers
normally transact in currencies familiar to their bank or corridor, with a smaller set
of alternative-currency cases. For treasury and liquidity stakeholders, the result
implies that currency demand can largely be planned from the sending network, while the
remaining 6–11% needs a separate corridor or customer-choice model.

Payment timing follows a related pattern. One shared weekly activity shape, shifted to
a different phase for each sender code, predicts July better than one global UTC profile
or separate customer-type profiles. This is consistent with institutions operating on
different market clocks and weekly schedules. Capacity planning should therefore align
staffing and liquidity buffers to sender-specific activity windows rather than one global
peak. The phases are only relative patterns learned from the data; without external
timezone evidence they must not be labelled as local timezones or business hours.

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
They do not recover every labelled event, and the `CUSTOMER_RECALL` mechanism remains
undefined and unresolved.

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
cannot separate true pair affinity from sender activity, receiver popularity, corridor
mix or observation-window effects, so July's longer observed gaps must not be presented
as evidence that customers slowed their payment activity.

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
are Covered overall, but a single global chance predicts July worse than an earlier-
fitted sender-code model: negative log loss **0.352294** versus **0.325958** on
1,065,699 rows (lead best-smoothed version **0.325912**). For 89 sender-country codes
with at least 1,000 rows in both periods, Covered rates range from 0.88% to 50.43%,
with early/July correlation **0.9973**. Adding FX and party type improves the lead
score to **0.324812**. A/B independently confirm the sender heterogeneity. Candidate
mechanism: after drawing more than two participants, choose Covered versus Indirect
with a stable sender-code-specific chance plus smaller FX/party adjustments. Banks,
corridors or currency zones nested inside sender code remain competing explanations.
Evidence: `a/covered_sender_debate.md` and B Covered review files.

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

## D2 · Processing time has several scales; simple delay formulas are insufficient

Direct routes with the same participant count range from seconds to hours. The
simple route/participant/FX linear model explains only **2.20%** of July duration
variation. Extra FX steps do not show a universal positive surcharge after the basic
route comparison; this does not prove that conversion makes payment processing faster.

A fitted two-group lognormal mixture outperforms a single lognormal or exponential
for several route-length groups. Continuous Direct p=2 July mean negative log-likelihood:
two-group **6.4471**, single-lognormal **6.8277**, exponential **7.4959** (lower is better).
The mixture still has substantial residual mismatch (total variation≈0.1325).
It is an improved predictive family, **not an identified exact delay rule**.

A/B exact conditional duration quantiles/means/counts reconcile (`verify_crosschecks.py`).
A fits the mixture on earlier observations and evaluates July. B independently rejects
simple fixed-delay interpretations using the same route/FX cells, but the exact
two-component parameters have not received a second blind fit. Bank-specific processing, country/currency
composition, queues and additional stages remain competing explanations. Mean increments
near 200 seconds on longer indirect paths are stochastic averages, not fixed per-payment
increments. Chart: [D2](charts/D2_duration_models.svg). Scripts/tables: A duration files,
B `b/duration_models.json`, exact conditional tables and logs.

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
may be unobserved or defined differently. Recall remains unresolved.

Full label/party census independently agrees: all 945 CEO labels have business senders;
all 2,476 romance labels have consumer senders, but **665 have business recipients**.
An exact consumer→consumer romance restriction therefore fails in this file.

## X2 · Text country tokens have asymmetric alignment

Ordering country token appears in **6,084,595** fields and matches the ordering-bank
country code in every one. Beneficiary token appears in **6,107,358** fields, but matches
its own bank country in only **59,826**. Missing-token fields have their own denominator.
Do not assume customer country equals bank country on the beneficiary side.

Lead full text census covers 20M fields. A/B independently parse raw token/bank columns
on all 10M transactions and agree on exact counts, including month/type strata; no
multiple-country-token fields observed. Debate/evidence: text initial records and scripts,
lead `text_round2.py` and `text/summarize.py`. Chart: [X2](charts/X2_country_tokens.svg).
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

## C2 · Currency choice is mostly sender-code-specific

Infer modal currency for each sender/receiver code from earlier payments, freeze it,
and evaluate July. Sender mode matches **2,592,753/2,899,279** (89.43%); either sender or
receiver mode matches **2,727,417** (94.07%). Lead/C independently implement the same
prediction on B's shared full-count table. A universal sender-mode currency rule fails.
Receiver mode means observed received-currency mix, not official currency. Bank-pair
and alternative-currency selection rules remain unresolved. Files: lead currency model,
C currency modes, B currency counts/initial question register. This is a high-accuracy
probabilistic rule, not a deterministic one.

## T2 · A common weekly schedule is shifted by sender code

On **2,896,968** complete-date July rows, an earlier-fitted pooled 168-hour UTC profile
has negative log loss **5.01885**. A separate sender-code profile improves this to about
**4.8765**. A compact model—one common weekly template with a circular phase for each
sender code—scores **4.87493**, slightly better than unrestricted sender-code profiles.
Party-type splits do not improve later-period prediction after sender code. A and B
independently reach the same result; the lead reproduces B's score.

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

## Remaining boundaries

The exact duration mixture, alternative-currency selection, full text grammar, ordinary
pair-affinity process and CUSTOMER_RECALL mechanism remain unresolved. Full historical
invoice matching beyond visible transfers is not possible from these tests. A fully
specified simulator also needs bank/corridor/entity-population rules that the observations
do not uniquely identify. These are supported partial or negative results, not gaps to
fill with guesses. Human interpretation and final deliverable selection remain future work.
