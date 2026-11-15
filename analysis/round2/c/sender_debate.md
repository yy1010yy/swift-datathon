# Same-sender history debate: C and independent B

Read B's `sender_initial.md` after C's `sender_romance_initial.md` and sender controls
were saved. B uses Decimal-derived integer cents and chronological timestamp-batch
updates; C uses integer-cent numeric vectors and strict-time masks. Both consume C's
shared full10M-source sender-history extract, so scoring independence does not remove
the common extraction dependency. The lead is verifying row-level indicators separately.

## Exact common result and deciding comparison

B/C agree on every reported target/control numerator and denominator. All7006 labels
are scored. The broad history condition is same sender/currency; exact account text is
preserved, target/control records see only strictly earlier timestamps, and controls are
the nearest preceding blank-label same-sender/currency row. Same-time control ties use
the smallest numeric source record; no observed within-timestamp order is claimed.

- FAT:23/1788 history-eligible target exact-power matches, versus32/1723 eligible
  controls. No support for the universal observed-prior-transfer decimal-shift rule.
- Replacement:8/603 eligible target exact-amount/different-beneficiary matches,
  versus12/591 controls. This simple invoice-replay comparison is not enriched.
- Recall:6/301 eligible target exact-amount/different-beneficiary matches, versus
 12/293 controls. This does not reconstruct an undefined recall mechanism.
- Duplicate:493/661 broad-history-eligible targets repeat an earlier amount to the
  same beneficiary, versus0/601 eligible controls. The narrower same-pair history
  denominator is515, with493 matches (95.73%); all labelled denominator is679,
  so recoverable exact replays are72.61%. These denominators answer different questions.

The deciding comparison is exact matched-row/summary reconciliation, followed by the
contrast with strictly earlier controls. Broad sender histories recover prior activity
for most cases, so lack of same-pair history is not simply lack of all sender history.
It still does not reveal an original intended invoice/amount for most labels.

## Strongest objections and scope boundaries

These controls are earlier blank-label payments, not known-legitimate payments. They
can be reused and have less accumulated history than their target; they are not matched
on payment purpose, amount or corridor. The chosen account/currency matching can miss
equivalent account formatting or conversion-related USD differences. Earlier invoices
and original intended amounts may never appear as separate records. A simple lack of
match cannot prove a label wrong or refute an error applied to an unobserved intended
amount. Recall is undefined by the supplied appendix, and no reverse-transfer mechanism
has been established. These comparisons are observational, not randomized causal tests.

## Narrow final wording

Observed-history replay is strongly supported for493 duplicate-labelled transfers,
with short preceding-match lags, and remains unresolved for the others. Simple visible
prior-invoice replacement and prior-transfer decimal-shift tests do not explain most
replacement/fatfinger labels. Neither negative test refutes latent corruption of a newly
generated intended payment. The separate FAT latent-distribution model provides a
plausible amount-distortion family; exact original amounts and shift probabilities
remain unknown. Recall remains an open label mechanism.

Evidence: B/C independent initials, scorer scripts, row-level outputs and summaries;
C `sender_controls_summary.csv`, `sender_summary.csv`, `history_summary.csv`; lead
row reconciliation when complete. Raw sender cache is ignored under `outputs/round2/c/`.
