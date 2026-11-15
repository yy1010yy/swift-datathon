# B sender-history and currency debate

Blind B initials are sender_initial.md and currency_initial.md. Only afterwards read
C sender_controls_summary.csv and currency_initial.md.

## Sender-history alternatives

C and B summaries agree in every label/target/control cell, including separate history
availability. The strongest objection to the earlier same-pair negative test was that
the intended predecessor might have a different beneficiary. Expanded same-sender/
currency history directly tests that objection and still does not support a universal
exact-decimal-shift rule: FAT23/1788eligible versus32/1723nearestearlierblankcontrols.
Nor does same-amount/different-beneficiary matching distinguish accountreplacement
(8/603target versus12/591control) or recall(6/301versus12/293).

These tests narrow the failures to **recorded prior-transfer replay/substitution models**.
They do not refute an error applied to an unrecorded intended amount, altered customer
identifier formatting, different-currency source, or history outside the observation
window. Controls have the same sender/currency and strictly prior time, but may differ
in payment purpose, amount, corridor and history depth. A prior blank label does not
prove legitimacy; controls can be reused. Do not treat target/control differences as
causal treatment estimates. Source ties are resolved explicitly, never by future rows.

## Currency mode preference

C independently implements the earlier-mode predictor on B's shared exact raw-scan
aggregate input. Correct July counts exactly match B: sender2592753/2899279,
receiver932564/2899279. C adds globalEURbaseline926598, showing sender-mode prediction
beats a dominantglobalcurrency explanation. Party strata preserve the sender advantage.

Final wording: payment currency is strongly associated with the sending side's learned
default; approximately89.4%of July records match the sendercountrycode's earlier modal
currency versus32.2%for the receiver-mode predictor. A universal sendermode rule fails
on306526Julyrows. No externally defined nativecurrency or exact90%injection probability
was inferred. Receiver-mode is received-traffic mix, not officialcurrency. The either-mode
coverage2,727,417 metric must not be called a single exanteprediction: selecting whichever
matches requires knowing the actualcurrency. Bank/corridor/customercomposition still
limits the causal story and country-specific exceptions require future testing.

Deciding comparison: earlier learned maps fixed before July, identical July populations,
sender/receiver/global alternatives, party strata and exact count reconciliation.
