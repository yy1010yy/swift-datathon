# UMDAC 2026 · Swift payments preliminary round

Use this checklist when working on the datathon. The team’s objective is to **reverse-engineer how the artificial payments were generated**. A finding should describe a candidate rule, the records where it applies, and the evidence for its limits. The current request expands work to sustained EDA and reconstruction of generating mechanisms across feature groups, including supported partial and negative results. Track code, actual outputs and methodology. PDF production has not started.

## Extended investigation · EDA phase complete

- [x] Run three independent full-file numeric investigations; exact blank-label amount quantiles reconcile across **1,228** currency×party×period cells and **9,992,994** rows. [Verification](analysis/round2/amount_verification.json). Preserve the caught `ALL`-currency/grand-total collision and correction in A's prior logs.
- [x] Independently reconcile continuous-route duration summaries and core strict-prior duplicate tests. [Cross-check](analysis/round2/crosscheck_verification.json); history uses C's shared extracted raw rows with independent A/B/C scoring (extraction itself not independently replicated).
- [x] Complete full-file text census over **20M party-detail fields**. [Code](analysis/text_round2.py), [tables/log](analysis/round2/text/), [full scan log](outputs/text_round2.log). A/B independent country-token checks agree; see the [extended evidence record](analysis/round2/findings.md).
- [x] Independently test a latent fat-finger amount model in A and C. Both find unusually wide adjusted amounts and improved July fit from decimal-shift mixtures; all 1,940 adjusted residuals reconcile in [verification](analysis/round2/fat_residual_verification.json). Exact shifts and independent debate remain unresolved. See `analysis/round2/a/fat_latent_initial.md` and `analysis/round2/c/fat_latent_initial.md`.
- [x] Recheck the candidate FX model against all 10M saved country sequences and reconcile 1,973 recurrence predecessor ratios with consistent tie handling: [verification](analysis/round2/fx_recurrence_verification.json). The refined FX fit uses exceptions and is not an untouched validation. Initial failed tie check is preserved.
- [x] Run anomaly same-pair history and broader sender-history tests, including selected unlabeled controls. [C method](analysis/round2/c/method.md), [results](analysis/round2/c/). Exact duplicate predecessors supported for a substantial subset; simple fat-finger/invoice-replacement hypotheses mostly unresolved/negative. Power-of-ten tolerance sensitivity is recorded separately; no hidden rounding discrepancy.
- [x] Routing/FX: reconstruct participant, gap, FX-zone, route-choice and endpoint-discrepancy mechanisms; A/B challenges, later-period checks and limits are recorded. Duration's simple additive model is rejected; exact mixture remains provisional.
- [x] Values/currency/timing: reconcile amount scaling across A/B/C; test earlier-fitted currency modes and independent weekly timing models. Alternative-currency selection remains unresolved.
- [x] Anomalies: complete strict pair and broader sender-history tests, latent fat-finger models, controls, tie audits and A/B/C review. CUSTOMER_RECALL remains an explicitly open mechanism.
- [x] Counterparties: C's full blank-label pair scan and B's independent regrouping agree on 9,992,994 rows, 8,258,480 pairs and 1,734,514 strict-prior rows. Homogeneous count/waiting models fail; the exact heterogeneous recurrence mechanism remains open.
- [x] Text/tokens: full-file census and A/B country-token checks complete. Exact text-generation grammar is an open partial result.
- [x] Exchange independent findings and run deciding/self-consistency comparisons for every promoted rule. Provisional items are labeled rather than silently promoted.
- [x] Consolidate methodology, executable artifacts and per-rule evidence in [extended findings](analysis/round2/findings.md), [evidence registry](analysis/round2/evidence_registry.md), and [code/output index](analysis/round2/README.md).
- [x] Add evidence-backed stakeholder business explanations for all eight headline finding groups in the canonical [findings report](analysis/round2/findings.md), clearly separating measured rules from plausible economic meaning.

## Current progress · 2026-11-14

- [x] Package this workflow as the reusable `reproducible-eda` skill: [team copy](skills/reproducible-eda/SKILL.md). Validated and installed in the personal Codex skills folder. It preserves executed outputs, question/theory records, independent review and plain-language explanations. Invoke with `$reproducible-eda` for upcoming analysis.
- [x] Read supplied case brief appendix and reconcile starting-point definitions and labels.
- [x] Create [question/theory register](analysis/questions.md) using comparison, trend, relationship, distribution and composition questions. Human owners remain unassigned.
- [x] Execute initial EDA on all **10,000,000** cleaned rows; preserve inputs and historical profile. [Executed notebook with code, outputs and charts](analysis/initial_eda.ipynb); [reproduction instructions](analysis/README.md); [run log](outputs/initial_eda_run.log).
- [x] Initial routing review R1/R1b and label coverage A0: two independent full-file analyses, exchanged debate, exact aggregate reconciliation and temporal stability checks. [Evidence/limits/final wording](analysis/progress.md), [A initial](analysis/reviews/a/initial.md), [B initial](analysis/reviews/b/initial.md), [A debate](analysis/reviews/a/debate.md), [B debate](analysis/reviews/b/debate.md), [verification](outputs/eda_initial/review_verification.json).
- [x] Save exact route, gap, diagnostic, FX, label, party-pair and UTC-time aggregate tables plus provenance in [initial EDA outputs](outputs/eda_initial/). FX/time tables are baselines only; no mechanism inferred.
- [ ] Assign human feature owners, deck editor and submission owner. Names are not available to the agent.
- [x] Complete endpoint, conditional FX/amount/timing, anomaly-history and counterparty investigations. Reviewed conclusions and remaining limits are consolidated in [one findings file](analysis/round2/findings.md).

**Reviewed initial results:** `participant_count` equals visible BIC **occurrences**, excluding `...`, in 10M/10M rows. Distinct-BIC counting differs in **59,191** rows. Gap presence agrees exactly with continuity N (**767,204** rows), so semicolon-token counts create that participant diagnostic; gaps do not explain every endpoint diagnostic. Six labels reconcile exactly, including **317 CUSTOMER_RECALL** records whose mechanism remains undefined. These are observed field/coverage relationships, not proof of the generator code or economic causality. See the evidence record for populations, exceptions and limits. UTC coverage includes a partial April 2023 boundary as well as May–July; monthly checks are retrospective, not an untouched holdout.

**Provenance correction:** The original `profile.json` contains a stale limitation saying duration and B/C meanings are undocumented. The appendix defines them. Preserve the historical file and use the corrections in `outputs/eda_initial/manifest.json` and the notebook.

## Competition criteria

Source: [Swift preliminary-round case brief](<C:/Users/yapka/Downloads/Universiti Malaya UMDAC Datathon 2026 - Swift Case Study Preliminary Round.pdf>), pp. 1–2. The appendix on pp. 3–4 defines the fields.

- [x] **Evidence scope.** All current findings derive exclusively from the supplied raw data and appendix definitions. No external GDP, timezone, currency or country-population data were used.
- [ ] **Dashboard PDF.** Aim for the expected **5–15 dashboards**, each covering one feature group. For every insight, state the reconstructed rule. Include at least one chart demonstrating the rules for each group. Several related charts can share a dashboard.
- [ ] **Slide deck PDF.** Prepare **10–20 slides total**, including introduction and methodology. Use **at most one summary slide per feature group**. For each principal insight, restate the rule, show or reference the dashboard chart, and explain the real-world economic behaviour it *may* represent. Describe how the analysis identified and tested the rules.

| Judging criterion | Weight | Proposed review question |
| --- | ---: | --- |
| Insight quality | 45% | Can a reader state the proposed generating rule, its direction, when it applies, and what it predicts? |
| Interpretation and economic reasoning | 12% | Does the explanation connect the observed pattern to a plausible decision by a sender, receiver, or bank? |
| Evidence, method and data integrity | 23% | Can another analyst reproduce the comparison, inspect exceptions, and see which alternative explanations remain? |
| Communication | 20% | Can a judge find the supporting chart and understand its population, units, and conclusion? |

The judges explicitly value analytically grounded partial and negative results. A candidate mechanism can earn a place in the submission even when the data leave its exact rule unresolved.

## Starting point

- [x] Cleaned and profiled all **10,000,000** records using [clean_data.py](clean_data.py). All rows were retained. The five numeric fields passed the implemented parsing and range checks. Use the [full profile](outputs/cleaned/profile.json) for counts and [cleaned data](outputs/cleaned/payments_cleaned.csv.gz) for analysis. The preview contains the first 1,000 rows.
- [x] Identified **1,665,936** records with at least one routing diagnostic and **7,006** with an anomaly label. These measure different things. Preserve repeated payments, unusual amounts, multiline text, and blank labels because they can carry evidence about the generator.
- [x] Apply the appendix when interpreting earlier cleaning notes. Duration is in **seconds**. B and C mean **business** and **consumer**. Amounts are normalized to USD. Tokens summarize patterns derived from the corresponding detail text. A path can contain a literal `...` gap, and `CONTINUITY_QFLAG` records observability. Counting semicolon-delimited entries as institutions can therefore mislead. Corrections recorded alongside initial EDA; historical outputs preserved.
- [x] Reconcile label coverage. Independently recount all 10M rows: six nonblank labels; appendix p. 4 describes five. Additional `CUSTOMER_RECALL` occurs **317** times. Its generating mechanism remains open. Blank labels retained as “no recorded anomaly label.” See notebook block 3 and `analysis/progress.md` A0.

## Who does what

At kickoff, put a teammate's name beside each feature group the team wants to investigate. One person can own several groups. Also name one teammate to edit the deck and one to submit the final files. These roles can overlap.

| Stage | 1. Humans (teammates) | 2. Lead agent and sub-agents | Handoff |
| --- | --- | --- | --- |
| 1. Frame the questions | Each feature owner writes a testable question, why a bank or customer might behave that way, and one observation that would challenge the explanation. Rank the questions together. | Map each question to available fields, comparison groups and units. Start from the existing cleaned file and profile. Identify where an assumption affects the test. | A prioritized question list with a human owner and a proposed comparison for each item. |
| 2. Investigate in parallel | Inspect example payments and their field definitions. Suggest competing business explanations and flag cases the aggregate might hide. | Run reproducible analyses. For every candidate insight, use the independent sub-agent debate and self-consistency procedure below. Quantify the relationship, exceptions and uncertainty. | The agent gives each owner a candidate rule, chart or table, calculation reference, strongest objection and self-consistency result. |
| 3. Select and interpret | The owner explains the chart in their own words and decides which economic interpretation they can defend. The team chooses which findings to present, qualify or set aside using the rubric. | Test outstanding objections and show how any revision changes the claim. Record supported limits and informative negative results. | A shortlist with agreed wording, supporting evidence and one stated limitation per claim. |
| 4. Build both PDFs | Feature owners write or edit the business explanation. The deck editor chooses the narrative order and which principal findings get a slide. | Produce charts, assemble the dashboard and slide deck, and link each slide claim to its dashboard chart. Recheck any materially revised insight. | Two draft PDFs for team review. |
| 5. Review and submit | Have a teammate outside each analysis explain its chart and challenge its conclusion. Feature owners resolve wording issues. The submission owner confirms organizer logistics, approves the final pair and submits it. | Recompute headline figures, reconcile the two PDFs, check group and slide limits, and inspect both rendered exports. Deliver the checked files and identify any unresolved limitations. | Final dashboard PDF and slide deck PDF, with submission confirmation recorded by the human owner. |

**First assignment.** A teammate can take routing and FX and ask how reliably visible BICs account for the reported participants. The agent can cross-tabulate visible BIC count against participant count by continuity flag and route type. The teammate then reviews example paths where counts differ and decides how to describe the role of gaps. Other owners can start their questions in parallel.

## Required review for every insight task

For each task that extracts or materially revises an insight, the lead agent must involve at least two sub-agents. Related candidate rules can share a review, but each rule needs its own conclusion. This is a team workflow requested by the user.

**Completed for initial batch R1, R1b and A0:** all four steps below; records linked in Current progress. The unchecked checklist remains a reusable requirement for each future insight task, not outstanding review of this batch.

1. [ ] **Independent analysis.** Give both agents the same question, field definitions, and data access. Have each return an initial conclusion, population, supporting calculation, and uncertainty before seeing the other's answer. Ask one to estimate the proposed relationship and the other to investigate a plausible competing explanation or counterexample.
2. [ ] **Debate.** Exchange the two findings. Have each agent respond to the other's strongest evidence and identify a comparison that could distinguish their explanations. The lead runs or verifies that comparison and resolves disagreements using the results. Record any question the available data leave open.
3. [ ] **Self-consistency.** For every candidate, including those on which both agents agree, compare the independently derived results on the same population. Reconcile denominators, units, effect direction, and magnitude. Test whether the conclusion holds under a relevant change of period, subgroup, or calculation where feasible. If it changes, document the boundary and narrow the claim or mark it inconclusive.
4. [ ] **Handoff.** In the evidence record for each insight, include both initial conclusions, the strongest challenge, a reference to the deciding calculation, the self-consistency result, and the lead's final wording. If a check could not be completed, record why and mark the finding provisional.

## Proposed analytical workflow

These are team planning choices. The feature groups and hypotheses can change as evidence comes in.

1. [ ] **Establish comparable populations (partially complete).** Initial EDA reconciles full-file counts, parses UTC, retains every row, counts valid visible BIC entries/gaps/distinct BICs separately and cross-tabulates all three existing routing diagnostics by continuity and routing type. Account-pair temporal features remain future work; keep account IDs as text and preserve repeated directed edges when implementing them.
2. [ ] **Test candidate rules by feature group.** Start with the comparisons below. Record the denominator and comparison group before interpreting a difference.

   | Feature group | First test |
   | --- | --- |
   | Timing | Compare UTC hour and weekday profiles within the same party-type pair and payment corridor. Check whether peaks recur in a later period. |
   | Currency choice | Compare currency shares for the same sender/receiver bank pair across party types. Report counts for sparse combinations. |
   | Payment values | Compare median and upper quantiles of USD amount within currency and B→B, B→C, C→B, C→C groups. Inspect repeated or rounded amounts and extreme values separately. |
   | Routing and FX | On continuous paths, compare participant counts and FX steps across Direct, Indirect, and Covered routes. Repeat on gapped paths to quantify the effect of observability. |
   | Duration | Compare duration in seconds for otherwise similar routes with differing participant or FX counts. Check whether apparent increments persist within routing type. |
   | Counterparties | Sort payments by time within a directed account pair. Compare repeat intervals and typical amounts with those of other pairs of the same party types. |
   | Party details and tokens | Trace selected token patterns back to the corresponding raw text. Measure how often formatting patterns recur within each party type. |
   | Anomalies | For each label, compare flagged payments with similar unlabeled records. For duplicate payments, look for an earlier matching transfer. For fat-finger mistakes, test power-of-ten amount changes against prior comparable amounts. Report cases with insufficient history. |

3. [ ] **Challenge each candidate.** Describe which feature could drive which outcome, test a simple competing explanation, quantify the effect and exceptions, and repeat on a held-out period or group where feasible. For historical features, use only information available before the payment. Distinguish deterministic relationships, probabilistic tendencies, and inconclusive tests.
4. [ ] **Record evidence for handoff.** For each candidate, record its feature group, rule in one sentence, population and exclusions, method or script, effect size with counts, validation result, exceptions, economic interpretation, and chart reference. A future contributor can pick an unchecked group and build on its existing evidence. Mark a test complete once its result can be reproduced, including a negative result.
5. [ ] **Build the dashboard PDF.** Select groups supported by evidence. Use a rule as the chart title where practical and label units, period, denominator, and comparison groups. Give each chart a stable reference for the slide deck.
6. [ ] **Build the slide deck PDF.** Select principal findings from those dashboards. Allocate introduction and methodology slides, then one summary slide per selected group. Use a conclusion or limitations slide where it adds information. Check the total against the brief.
7. [ ] **Review both exports together.** Recompute headline figures, trace each slide claim to its dashboard evidence, verify page and slide counts, and open both PDFs to check legibility. Review against the four weighted criteria before marking either deliverable ready.
