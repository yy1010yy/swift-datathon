# B independent recurrence/escalation initial result

Computed before receiving C's recurrence/escalation figures. Shared extracted raw
history22523rows, independently sorted within exact directed account pair and currency
by timestamp then numeric source_record. For each timestamp batch, latest predecessor
has a strictly earlier timestamp; ties at the predecessor timestamp choose maxsource.

Of2,476 ROMANCE_SCAM payments,1,973 have such a predecessor. All1,973 follow within
one hour: median215seconds,10th32.2,90th709.8. Current/latest-prior amount ratio
has median1.5,p10=.894982,p90=2.489667.1,639 increase,323 decrease,11 equal. Thus
rapid recurrence and a typical increase are supported in observed histories, but
strict monotonic escalation is false. Remaining503 lack a strict same-pair/currency
predecessor in this selected observation window.

No-recorded-label controls in these selected pairs:14,788 with prior; median lag
14,410.5seconds, median ratio.973219,7,324 increase/7,446 decrease/18equal;4,569
within an hour. This is history-selected, not a representative or causally matched
control. Need compare within same pair/customer type/time/history depth to separate
scam injection from legitimate recurrent transfer schedules.

DUPLICATE_PAYMENT known-history rows515:median lag1163seconds,493 latest-prior
equal amounts,454within an hour. Other labels have sparse histories; fatfinger
current/latest ratio median88.974 is broad and does not replace the failed exact
power10 test. Saved row evidence history_lag_rows.csv and summary history_lag_summary.csv.
