# A independent Covered/Indirect sender-code review

Own numpy-bincount target encoding on shared B full numeric cache uses pre-July
2,611,021 nonDirect routes, evaluates1,065,699 July routes. Alpha100 is fixed before
the calculation, rather than selecting the best July score. Constant NLL.352294411;
sender-country-like-code NLL.325958062, gain.026336349nats. Lead's best-alpha result
.325912 is close; smoothing choice explains the difference. One July row has a
sender absent from early nonDirect training and falls back to global probability.

Among89 codes with>=1000 early andJuly records, early Covered probabilities range
.00881–.50430; early/July rate correlation.99728 and weighted absolute rate change
.00178. This is stable heterogeneity, not merely rare-cell noise. Source-level tables
retain sparse codes and periods instead of discarding their uncertainty.

Deciding comparison disproves a universal independent Covered probability: sender
conditioning predicts better on later observations. Earlier fixed-P/FX comparisons
also reject constantprobability, and the lead's sender+FX/party models improve further.
The geometric participant-count mechanism remains a separate well-fitting rule;
it does not imply that route-label choice is independent of customer/bank features.

Strongest alternative is bank or currency-zone mixture nested inside sender codes.
This cache does not contain individual orderingBIC/beneficiaryBIC, so these fits cannot
distinguish a direct country-level draw from bank-level rules or corridor preferences.
Country-like codes may serve as generator inputs, but predictive value alone does
not establish that causal role. Never interpret the synthetic code rates as actual
country banking metrics.

Final wording: **For routes with at least3 visible participants, the chance of a Covered
rather than Indirect label varies substantially and stably across sending-bank country
codes. A sender-code-specific probability predicts July better than one global chance;
the underlying bank/corridor mechanism remains unresolved.**

Reproduction: `covered_sender_review.py`, actuallog, stabilityCSV and summaryJSON.
