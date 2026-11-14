---
name: reproducible-eda
description: Conduct or continue exploratory data analysis with executed code outputs, a question and theory register, independent review of proposed findings, and plain-language explanations. Use for dataset investigations and reverse-engineering data-generation rules, especially the Swift payments datathon.
---

# Reproducible EDA

Produce an investigation teammates can inspect and continue: the question asked,
code actually run, results, competing explanations, and limits of each conclusion.
Respect the requested stage. Initial EDA does not authorize a final deck, dashboard,
model, or submission.

## Resume before expanding

Read the project's `AGENTS.md`, existing progress/evidence records, data definitions,
profile and analysis scripts. Reuse completed work instead of rerunning every scan.
For this Swift datathon, read [references/swift-payments.md](references/swift-payments.md).
Use its facts as prior context; verify against current artifacts before making new claims.

Find the next unfinished task within the user's scope. Record what is already verified,
what is provisional, and what remains untested. Do not invent human owners or business
definitions. Preserve historical results; put corrections in a dated note or manifest.

## Frame the question before calculating

Maintain a question/theory register for each feature group being investigated. Use
comparison, trend, relationship, distribution or composition as helpful lenses, rather
than forcing all five onto every question. Each entry needs:

- A specific question, fields, units, population, exclusions and comparison group.
- A measurable outcome: count, share, conditional quantile, amount ratio, interval, etc.
- The analytical or business decision the answer would inform.
- A possible generating rule, plausible business explanation, competing explanation,
  and an observation that would challenge the proposed rule.
- Priority, status and human owner if known.

Separate what the data show from what might explain it. Names of fields or labels
alone do not establish their generating mechanism. Partial and negative results can
be useful findings when the test and limits are clear.

## Keep code and its results together

Save executable analysis code and actual outputs for every substantive analytical
block. Prefer an executed `.ipynb` with short question/method notes, code, tables,
charts and checks. A script plus a clearly indexed report and saved result tables is
also acceptable. An empty notebook or code with manually invented outputs is not.

For a notebook generated without Jupyter, execution counts and output cells must
come from real executions. Capture failures as failures. Store failed attempts and
the correction when they materially affect the analysis; never present partial output
as a completed full-file scan. Make notebook cells runnable in order from a documented
working directory. Prefer helpers over copying large scripts into several artifacts.

Save exact CSV/JSON aggregates beside charts. Give results stable IDs and link each
claim to its code block, table, chart and review. Include reproduction commands,
dependencies, input identity, row count, time coverage, run date and completion status.
Explain whether input identity is a content checksum or only file size/modification time.
Mention ignored output directories so teammates know what must be regenerated/shared.

## Establish trustworthy comparisons

Use full-file profile totals as controls. Chunk large files; label samples and their
selection method explicitly. Never generalize from a first-N preview as though it were
random. Preserve account IDs as text, literal codes, quoted multiline CSV content,
repeated transfers, blanks and extreme values unless the user requests a transformation.

Parse numeric/time fields explicitly and check failures. State time zone and units.
Separate visible entries, distinct entities and placeholders when parsing sequences.
Treat diagnostics as questions to investigate, rather than automatic reasons to delete
rows. Reconcile denominators before interpreting differences.

Condition comparisons on plausible drivers instead of relying only on aggregate means.
Inspect tails, sparse cells, exceptions and alternative definitions. For histories, use
only information available before each event. Distinguish a retrospective stability
check from a genuinely untouched validation sample. Exact full-population counts need
no sampling interval, but they do not guarantee generalization to other populations.

## Review every new or materially changed finding

For insight extraction under this workflow, use at least two independent sub-agents.
Related rules may share a review, with a separate conclusion for each. Routine artifact
inspection or explaining an already verified result does not require a fresh review.

1. Give both agents the same question, definitions, population and data access. Ask one
   to estimate the proposed relationship and the other to test a plausible alternative
   or counterexample. Keep their initial results independent until both have returned.
   Preserve each initial conclusion, supporting calculation, denominator and uncertainty.
2. Exchange their findings. Each responds to the other's strongest evidence and names
   a comparison that could distinguish the explanations. Preserve the debate responses.
3. Run or verify that comparison. Match their independently derived results on the same
   population: denominators, units, direction and magnitude. Compare exact joint tables
   where feasible, not just rounded percentages. Repeat by a relevant period, subgroup
   or calculation. Record sparse/boundary cases and narrow claims that fail a check.
4. Save the final wording, strongest challenge, deciding calculation, self-consistency
   result, exceptions, interpretation and unresolved questions. If agents or a necessary
   check are unavailable, document why and mark the finding provisional.

The lead resolves differences with evidence; agent agreement alone is not validation.
An observed deterministic relationship does not prove the generator's source code or
the direction of causation. Label probabilistic tendencies and inconclusive tests plainly.

## Maintain the handoff and explain simply

Update `AGENTS.md` with completed tasks, artifact links, next steps and open questions.
Link detailed evidence rather than copying every result into the checklist. Mark only
the current batch complete; leave reusable review requirements for future batches.

For each finding, teammates should be able to find: its ID and question; proposed rule;
population/exclusions; calculation and actual result; both initial reviews; debate and
deciding test; stability result; limits; possible business meaning; and chart/table link.
Descriptive baselines must be distinguished from reviewed generating rules.

Explain the result in everyday language. Start with what we learned, give a tiny
concrete example, then the measured support and what remains unknown. Define necessary
terms where used. For routes, show a short bank sequence; for ratios, show two amounts.
Avoid leading with large counts or jargon. Keep the explanation consistent with the
saved evidence, and do not turn a possible economic story into a demonstrated fact.
