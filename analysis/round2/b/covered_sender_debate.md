# B conditional routing-choice review

Question: once a route has more than two visible participants, is Covered versus
Indirect simply a constant-probability choice? The unified length rule is separate:
Direct iff participant count is two is exact in all10Mrows. This review concerns only
2,611,021earlier and1,065,699July nonDirect payments.

B independently reimplemented the prediction from its full numeric cache, aggregating
success/failure counts rather than using the lead's row-level lookup implementation.
For each earlier group estimate `(Covered count + alpha × global Covered share) /
(group count + alpha)`. New groups fall back to the earlier global share. Compare
alpha10,100,1000 transparently; the best-alpha July score is descriptive model selection,
not an untouched evaluation after all choices were fixed.

| Earlier grouping | July logloss, alpha100 | Best displayed sensitivity |
|---|---:|---:|
| One constant fraction |.352294|.352294|
| Participants and FX count |.352005|.352005|
| Payment currency |.341718|.341684|
| Sending-bank country code |.325958|.325912|
| Sending code and FX |.325712|.325407|
| Sending code, party pair and FX |.325627|.324812|

Scores reproduce the lead's calculations. Country-group membership explains more
of the later-period choice than participant count, FX count or payment currency alone.
This challenges both a universal11.3%Covered draw and a claim that current currency
mix alone explains route choice. It does not establish that sender geography is an
explicit generator input: country code can stand in for banks, currency zones,
corridors, customer populations or route-construction rules.

Sparse-cell accounting: sender-only has226earlier groups, one July payment with an
unseen group, and430payments in groups with fewer than100earlier observations.
Currency-only has153groups,5unseen payments and278rare-group payments. The largest
sender/party/FXmodel has6261groups,377unseen payments and32811rare-group payments;
fallbacks and smoothing remain explicit. Thus broad sender-model improvement is not
an artifact of dropping unseen payments, though detailed-cell gains can overfit.

Strongest remaining alternative: unmeasured sender-bank/receiver-bank/currency-zone
mixtures produce a stable country association without a country-specific Covered
coin. The cache lacks receiver codes and individual bank identities, so this analysis
cannot separate those mechanisms or identify causal ordering between FX and route
category. Full-country default-currency and payment currency are different controls.

Final wording: **Longer routes are not assigned Covered versus Indirect by one
fully recovered universal probability. The overall Covered share is about11.3%,
but sending-bank country-code groups improve prediction materially and FX-conditioned
exceptions persist. Which bank/corridor decision creates this variation remains open.**

Evidence:covered_sender_check.py,covered_sender_scores.csv,covered_sender_cells.csv,
actual covered_sender_run.log. Keep the accurate geometric length model and this
partially unresolved route-category mechanism as separate conclusions.
