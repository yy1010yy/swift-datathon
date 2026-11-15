# B independent sender-history/control initial

Written from sender_review.py outputs before reading C sender summaries or controls.
Shared C full-source extraction; independent Decimal-cents scorer and chronological
batch updates. Same sender and payment currency; account strings preserved. Exact
power-of-ten amounts use exponents±1…6 with no cent tolerance. All7,006labels scored.
Each target's control is nearest strictly earlier blank sender/currency record; a control
sees only its own strict past. Timestamp ties choose smallest numeric source record.

| Label | Target n | Target with past | Exact same/different receiver | Exact power10 | Available controls | Controls with past | Control same/different | Control power10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| FAT_FINGER_MISTAKE |1940|1788|0/16|23|1787|1723|1/34|32|
| ACCOUNT_REPLACEMENT_SCAM |649|603|0/8|5|603|591|0/12|9|
| CUSTOMER_RECALL |317|301|0/6|7|301|293|2/12|4|
| DUPLICATE_PAYMENT |679|661|493/13|16|619|601|0/8|7|
| CEO_SCAM |945|822|0/9|7|822|765|0/15|10|
| ROMANCE_SCAM |2476|2066|12/0|0|477|243|0/4|0|

The expanded sender history does not rescue a universal prior-transfer decimal-shift
rule for fatfinger labels:23/1788targeteligible versus32/1723eligible earliercontrols.
Likewise accountreplacement has8/603eligible exactamount/differentreceiver matches
versus12/591controls, and recall6/301 versus12/293. These are informative negative
tests of narrow observed-history mechanisms, not proof the labels or intended latent
mechanisms are incorrect. A sender may have many unrelated payment purposes; controls
are nearest-in-time, not guaranteed legitimate or amount/corridor matched. Controls can
be reused and have less accumulated history. Availability and eligible denominators
are reported separately; target denominators cannot be replaced by control counts.

Saved row indicators, summary and manifest:sender_independent_rows.csv,
sender_independent_summary.csv,sender_manifest.json; actual log sender_review_run.log.
