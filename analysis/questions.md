# Initial EDA questions and theory register

Scope agreed 2026-11-14: complete starting-point checks and begin EDA. No dashboards,
deck, model training, deduplication or anomaly-history inference in this pass.
Human owners, deck editor and submission owner remain **unassigned**; no names invented.
Priority is analytical order, not a claim about business importance.

Evidence policy: only supplied payments establish findings. Appendix definitions guide
interpretation. Economic explanations below are hypotheses, not external evidence.
Use full populations, record exclusions and counts, and preserve blank labels and repeats.

| ID / priority | Feature / question framework | Specific measurable question and comparison | Meaningful next action | Status |
|---|---|---|---|---|
| R1 / 1 | Routing / relationship, comparison | Within continuity flag × Direct/Indirect/Covered, what fraction has participant_count equal to valid visible BIC **entries**, and what is the participant-minus-visible distribution? Contrast distinct BIC count and repeat by month. | Decide when visible routes can support participant/FX/duration tests. | Initial full-file EDA and independent review this pass. |
| A0 / 1 | Anomalies / composition | Among all 10M rows, how many have each nonblank label and how many have none? Which labels lack an appendix definition? | Establish label denominators before mechanism tests. | Reconciliation this pass; mechanism unresolved. |
| T1 / 2 | Timing / trend, comparison | Within party pair and ordering/beneficiary bank corridor, do hourly and weekday UTC shares change between May–June and July? Divide by observed calendar exposure, flag partial boundary days; show counts. | Identify recurring schedules worth modelling. | Hour/weekday × party counts saved as baseline only; corridor and exposure tests pending. |
| C1 / 3 | Currency / composition, comparison | For the same directed bank pair, how do payment-currency shares differ across B→B/B→C/C→B/C→C? Show cell counts and compare large cells first. | Separate corridor mix from customer-type preferences. | Planned; no conclusion. |
| V1 / 3 | Values / distribution, comparison | Within currency × party pair, how do USD median, p90 and p99 differ? What fraction has round-dollar amounts? Repeat with labels stratified and later-period validation. | Choose plausible amount distributions and isolate tail mechanisms. | Only full-population min/max/mean controls now; quantiles pending. |
| R2 / 2 | Routing/FX / relationship | Within continuity × route type × participant count, what is the distribution of FX steps? Do impossible-looking counts occur only on gapped paths? | Define comparable route populations before proposing a conversion rule. | Joint counts saved; interpretation deferred. |
| D1 / 4 | Duration / relationship | Within continuous route type and FX count, how do duration medians/quantiles differ by participant count? Test additive increments against route-mixture explanation and repeat by month. | Estimate a candidate delay mechanism in seconds. | Full-file range/mean control only; inference pending. |
| P1 / 4 | Counterparties / trend, distribution | Within each directed account pair, what are preceding-payment intervals and amount ratios, compared with other pairs of the same party types? Report pairs with insufficient history. | Distinguish recurrence from independent transfers. | Planned; account IDs stay text; no sequence inference yet. |
| X1 / 5 | Details/tokens / composition, relationship | How often do selected token patterns match their corresponding raw-text features within each party type? Check multiline and formatting exceptions with source record references. | Explain text generation and avoid treating derived tokens as independent evidence. | Planned; examples must be traced to original details. |
| A1 / 5 | Anomalies / comparison, trend | For each documented label, what fraction matches a prior comparable payment or prior amount × power of ten? Use strictly preceding history, matched party/corridor controls and insufficient-history denominator. | Test label-specific injected mechanisms. | Planned; recall remains an undefined category. |

## R1: theories, tests and boundaries

Population: all retained rows, stratified by flag and route type. USD amounts and
customer text are irrelevant to this initial encoding test. `...` is a placeholder,
not an institution; a repeated BIC is a repeated visible entry. A valid BIC entry
here matches `[A-Z0-9]{8}`; unknown/empty entries are counted separately, not silently dropped.

Candidate theory: complete routes expose participant entries; incomplete paths hide
some participation. Possible business meaning: observability differs along correspondent
chains. This does **not** identify which banks were hidden or the reason for a gap.

Competing theories: participants count unique institutions; each placeholder stands
for exactly one bank; routing type alone explains mismatches; endpoint diagnostics
measure bad data. Challenge these with distinct-versus-entry counts, participant-minus-visible
distribution, type/flag cross-tabs, and month strata. Counterexample: any continuous
route with a count mismatch refutes an exact complete-path rule. A nonzero endpoint
diagnostic on an ungapped path challenges an explanation based solely on gaps.

Methods: `run_initial_eda.py` blocks 2/4/5; independent `review_a.py` and `review_b.py`.
Examples are the first two per observed flag/type/difference class, explicitly illustrative,
not a representative sample. Only observed months are tested; no guarantee outside this file.

## A0: theories, tests and boundaries

Population: all rows, including blank strings. Compare exact counts to historical profile.
The appendix documents five labels; `CUSTOMER_RECALL` is an additional observed code.
Possible theory: a separate customer-initiated reversal process; **untested and undefined**.
No recorded label does not establish that a payment is legitimate. A label count alone
does not reconstruct how the anomaly was generated. A prior matching transfer would be
necessary evidence for a recall theory; it may still be insufficient to identify intent.

## Theories to revisit in later feature work

- **T1:** scheduled customer activity may create repeatable timing profiles. Corridor mix,
  partial-day exposure and UTC/local-time differences could produce misleading peaks.
  A peak disappearing within corridors or in July challenges the scheduling theory.
- **C1:** banks/corridors may constrain currency choice. Party-type mix could explain
  apparent preferences. An effect vanishing within bank pairs weakens a customer-type rule.
- **V1:** business purposes may create different amount scales; heavy tails, currency mix
  or labeled injections may dominate means. Similar conditional quantiles challenge the claim.
- **R2:** intermediaries may offer more conversion opportunities. Routing design and hidden
  path sections are alternatives. Counts alone cannot establish which institution converted.
- **D1:** processing stages may add delay. Route type, FX and timestamp mix could confound it.
  Nonpersistent increments within route/FX strata challenge a universal additive rule.
- **P1:** payroll/invoice/remittance schedules may cause recurring edges. Account popularity
  and random coincidences are alternatives; use same-type controls and only past information.
- **X1:** party-type-specific formatting may drive tokens. Tokens are derived from text,
  so agreement is an encoding result, not two independent pieces of business evidence.
- **A1:** labels may mark deliberate modifications of earlier payments. Sparse history and
  legitimate repetition challenge this interpretation; no-history cases remain unresolved.

Each later candidate requires its own two-agent initial conclusions, debate, deciding
calculation, self-consistency check, limits and final wording before handoff.
