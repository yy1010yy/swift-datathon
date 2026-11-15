# D blind initial: CEO, account replacement and customer recall

Saved before reading C's round-3 conclusions. Two independent full 10M raw scans found
all 1,911 target rows and 2,548,692 rows involving their endpoint accounts. Histories
use exact raw accounts/currency and timestamp strictly less than the query. Each target
uses its nearest earlier blank same-sender/currency record as control when available.

## Account replacement

None of 649 targets pays a recipient account previously seen for that sender/currency;
603 have some prior sender history. Controls revisit an account in 90/603 cases. Only
49/649 targets reuse a recipient BIC, so the universal story “same beneficiary bank,
different account” is false. Amount rank and amount/prior-median ratio are nearly the
same as controls (median percentile 0.50; ratio 1.012 versus 1.004).

Candidate rule: force a novel recipient account, not necessarily within the old bank,
while drawing an otherwise ordinary-sized payment. This is consistent with redirection
to replacement details but cannot identify an invoice or intended original account.

## CEO scam

Only 2/945 targets revisit a recipient account and 62/945 reuse a beneficiary BIC.
Among 822 targets with prior sender/currency history, median amount rank is the 71.2th
percentile and median amount/prior median is 2.63, versus 51.7th percentile and 1.12
for 822 selected controls. All CEO senders were already known to be businesses.

Candidate rule: a business sender pays a nearly always novel recipient and draws a
larger-than-usual amount for that sender/currency. Novel recipient alone can occur in
ordinary first payments, and controls have earlier positions/shallower histories, so
this is a strong signature rather than proof of social-engineering intent.

## Customer recall

Recall targets closely resemble controls: prior account 59/317 versus 58/301; prior BIC
151/317 versus 144/301; median amount percentile 0.498 versus 0.516; amount/prior median
0.875 versus 1.131. Only one target has any earlier reverse-direction same-pair payment,
none has an exact reverse amount; controls have two and none exact. Exact prior outgoing
amounts are also less common in targets (6) than controls (13).

No visible-history recall mechanism is recovered. The label may refer to post-payment
action, a latent instruction or information absent from the file. Inferring reversal
from the name is contradicted by the tested histories.

Evidence: `anomaly_review.py`, actual log, `anomaly_rows.csv`, `anomaly_summary.csv`
and manifest. Cancelled inefficient scorers are preserved and produced no result.
