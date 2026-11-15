# Round 3 B: independent questions and challenge design

Saved before reading any other round-3 agent output.

## Bank and corridor rules

Population: supplied 10M payments; pre-July estimates evaluated on July. Exact BIC8
strings are preserved. Amount models exclude nonblank anomaly labels; timing uses only
complete May 1–July 30 UTC dates. Outcomes and units are payment currency, log USD
amount, Covered vs Indirect among non-Direct routes, 168 UTC hours of week, and log
duration in seconds.

Question: after known country, currency, party, route, FX and participant effects,
does exact sending bank, receiving bank or directed bank pair add stable later-period
prediction? A generator-level bank/corridor rule is supported if an earlier-fitted exact
identifier model improves July prediction with shrinkage and adequate coverage. It is
challenged if gains disappear versus country/role baselines, occur only in rare cells,
or fail later-period evaluation. Bank identity may proxy an unobserved corridor or
customer mix; prediction does not establish causal direction.

## Entity, relationship and correspondent-network formation

Population: all endpoint banks for activity/network summaries; blank-label directed
account pairs for recurrence when using the existing raw-partition extraction. Visible
route BIC occurrences remain occurrences, and `...` remains a gap rather than a bank.

Questions: are bank/account activity and partner degrees sufficiently heterogeneous to
explain the repeated-pair tail without pair affinity? Does a sender/receiver-activity
independence benchmark reproduce observed repeat counts? For routes with at least three
visible BICs, is the first intermediary drawn globally or from stable sender/currency/
endpoint-specific pools?

Candidate business explanation: high-activity institutions, popular receivers and
currency-specific correspondent hubs create much of the observed network structure.
Competing explanation: durable pair-specific relationships and exact corridor routing
remain necessary after activity controls. A deterministic-hash sample or shared prior
extraction must be labelled; no sample is treated as a full random census.
