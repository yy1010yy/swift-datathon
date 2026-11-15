# B independent history result before reading C history conclusions

Population:22,523 extracted records in exact directed account-text pairs with at least
one label; shared C extraction, independently reimplemented scoring. No independent
second extraction claimed. Compare same pair/currency with strictly earlier epoch
timestamp; equal-time rows are inserted only after evaluating their timestamp batch.
Decimal source amounts convert to integer cents. Decimal shifts±1…6 allow one target cent.

| Label | Rows | With strictly prior same-pair/currency | Exact earlier amount | Power10 earlier amount |
|---|---:|---:|---:|---:|
| no recorded label |15,517|14,788|209|548|
| ACCOUNT_REPLACEMENT_SCAM |649|0|0|0|
| CEO_SCAM |945|2|0|0|
| CUSTOMER_RECALL |317|59|0|0|
| DUPLICATE_PAYMENT |679|515|493|0|
| FAT_FINGER_MISTAKE |1,940|313|0|3|
| ROMANCE_SCAM |2,476|1,973|12|3|

Candidate duplicate replay mechanism strongly supported in observed histories:
493/515 known-history duplicate labels repeat an exact amount.164/679 lack strict
earlier same-pair/currency history; absence cannot refute an out-of-window source or
an account-format variant. Unlabeled selected-pair controls have209/14,788 exact matches;
these controls are history-selected and not a causal matched population.

The narrow fat-finger hypothesis (prior amount on same exact pair/currency differs
by a power of10) has3/313 matches with observed history, not a general explanation of
the1,940 labels. Could be changed amounts drawn independently, another prior sender
recipient, out-of-window source, or injected from an unsupplied latent base. Label name
does not resolve that. Recall mechanism not recovered by exact/power10 pair-history tests.

Scoring saved in history_independent.py, history_independent_rows.csv and
history_independent_summary.csv; actual successful log history_fast_run.log.
Original slower all-priors implementation preserved in history_slow_attempt.py and
history_run.log. Faster version searches exact admissible integer-cent intervals using
bisect; it changes computation speed, not the definition of a match. history_n is count
of distinct preceding cent amounts, used here only as a nonzero-history indicator.
