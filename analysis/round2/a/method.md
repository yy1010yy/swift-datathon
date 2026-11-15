# Independent reviewer A — round 2

Questions recorded before seeing other reviewers' results:

1. **R2:** Does FX count equal adjacent visible BIC-country-code changes? If not,
   which directed country/payment-currency combinations refute that rule? Full
   route/continuity/participant/month cross-tab; restrict exact path transition tests
   to continuous paths because collapsing gaps connects nonadjacent visible banks.
2. **D1:** Is duration an additive function of participants, FX or route category,
   or is a mixture of fast and slow processing needed? Compare full conditional
   distributions, not just pooled correlations. Discovery before July 1, July check.
   Continuous and gapped paths are separate populations.
3. **R3:** Are endpoint mismatches compatible with independent roughly 5% changes
   at each end, or do route/continuity/month strata reject this proposed mechanism?
   Independence can fit probabilities without identifying the cause of substitution.
4. **V1:** How do full-population conditional USD quantiles and log-amount moments
   differ by party pair and currency? Remove recorded anomalies only for this base
   amount-distribution comparison, explicitly count that exclusion; label-free rows
   are not proven normal. Repeat early/July to distinguish changing mix.
5. **A1:** Which sender/receiver party restrictions do the supplied labels satisfy?
   This is a necessary condition for the label descriptions, not reconstruction of
   historical fraud or error mechanisms.

Business theories: conversion follows currency boundaries rather than just bank
count; processing stages may add independently sampled latency; route observability
may affect reported length; business transfers may use larger amount distributions.
Challenges: country codes need not uniquely identify currencies; gaps hide transitions;
FX and participants co-vary; route composition can confound delays and amounts.
No external currency/country mapping is used. BIC country-like code is positions 4:6.

`analyze.py` reads all 10M logical CSV records in bounded chunks and writes exact joint
counts plus an ignored numeric memmap. `summarize.py` computes exact conditional
quantiles/moments from that full population, rather than a preview sample. Actual stdout
is in `run.log` and `summary.log`. Numeric cache/histogram lives in `outputs/round2/a`;
the small evidence tables live beside this document for team sharing. Preserve supplied
dataset disclaimer when sharing externally.

Early/July comparisons here are retrospective stability checks, not an untouched test set.
The scripts preserve original input and every row; they do not infer causal direction
from association or assume a label name proves an injection mechanism.
