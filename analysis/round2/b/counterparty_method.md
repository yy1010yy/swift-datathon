# B independent general-counterparty review method

Question: among payments with no recorded anomaly label, how many exact directed
account pairs recur, and can a homogeneous payment-count or waiting-time model explain
the within-party-group distribution? Blank labels do not prove legitimacy.

Use C's32 raw-record partitions covering all9,992,994blank rows, without reading C's
conclusions or summary counts. This shares filtered raw extraction, not scoring logic.
Partition hashes only route records to files; complete raw sender/receiver strings
remain the grouping identity. Currencies are pooled for this general directed-edge test.
No first-N sample, identifier normalization or observed-repeat removal.

Independently group each partition by full raw sender/receiver strings, count full and
preJuly/July appearances, and mark inconsistent role pairs MIXED. Recompute singleton
versus repeated-pair counts and early-only/both/July-new cohorts. Distinguish payments
in recurring pairs from the number of later repeat events: these have different units.

For histories, independently reduce to unique pair/timestamp rows, shift timestamps
within each pair, then join the latest strictly earlier distinct time to every original
row. Same-time rows do not count as past. First-timestamp rows have no observed prior;
later tied rows share the same true preceding timestamp. Assign an interval to the
period of its later payment, retaining preJuly-to-July histories.

Fit zero-truncated Poisson and positive-geometric counts separately by role/period.
These are observed-pair count families, not probabilities of making any payment;
potential absent pairs are unknown. For positive intervals, fit one exponential mean
on earlier data within each role and compare the same bin probabilities on July.
Exact quantiles/count histograms and binned model total-variation errors are saved.

Main alternatives: activity-rate mixtures, customer popularity, bills/payroll schedules,
bursts, calendar-volume changes, or identifier formatting. Full-window pair counts
cannot distinguish these. Left censoring hides earlier payments; right censoring hides
later payments/long waits; finite maximum duration caps observable gaps. July observed
pair selection differs from the earlier cohort, and recurring-pair histories are a
selected subset. Model failure is an informative negative result, not proof of a
specific alternative generator. Raw account keys do not automatically establish
stable real-person identities or bank-qualified uniqueness.
