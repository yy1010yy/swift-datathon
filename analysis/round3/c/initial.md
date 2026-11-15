# Round 3 C independent initial conclusions

Saved before reading A/B round-3 results. The bank cache is an independent 10M-row
raw scan; duration/currency outcomes reuse A's aligned numeric cache, with C's own
model implementation. Anomaly histories reuse C's prior full-source sender extract.

## C-A1 · CEO and replacement labels create novel recipients; recall remains invisible

The three target/control populations were scored with only strictly earlier timestamps,
exact raw sender/account strings and the same currency. Controls are the nearest earlier
blank-label same-sender/currency rows selected in round 2, then rescored using their own
past. They are not randomized and generally have less accumulated history.

**Account replacement.** All **649/649** labelled target recipient accounts are new to
that sender/currency history. History is available for 603 targets. Only **49/649** have
a previously seen recipient BIC with a different account, so a universal “same bank,
replace only the account” rule is false; most rows replace or introduce the wider
recipient endpoint. Controls repeat a prior exact recipient account in **90/603** cases
and have a seen recipient BIC in **293/603**, versus target **0/649** and **49/649**.
Target and control amount medians are both near the prior median (1.012× vs1.004×), so
amount distortion is not the main visible signature.

**CEO scam.** All 945 have business senders from the earlier verified composition. Only
**2/945** target recipient accounts and **62/945** recipient BICs were previously seen,
versus **102/822** and **324/822** in controls. Among the 822 targets with prior history,
the median amount is at the **71.2th prior percentile** and **2.63×** the sender's prior
median; controls are at the51.7th percentile and1.12×. Candidate mechanism: choose a
business sender, introduce an almost always novel recipient, and draw an elevated but
not fixed amount. Novelty could partly reflect later/deeper histories or ordinary new
payees; the control direction actually makes the target contrast conservative on depth,
but it is not a randomized causal comparison.

**Customer recall.** Target and control features are close: prior account seen59/317
versus58/301; BIC seen151/317 versus144/301; median amount percentile.498 versus.516;
median any-payment lag13,206s versus15,895s. No exact-amount reversal or visible-history
signature is enriched. This is a supported negative result: the current transaction
fields do not reconstruct recall. An external request/event or status absent from the
file could carry the mechanism.

Evidence: `anomaly_initial.py`, actual log, `anomaly_history_features.csv`, summary and
manifest. Insufficient-history counts remain explicit.

## C-D3 · Duration is largely bank-specific on the log scale

Models were fit on7,094,560 complete-date May–June rows and frozen for2,896,968 July
rows. Route+participant+FX alone gives July log-duration R² **0.0464**. Adding sender
and receiver country raises this to **0.1188**. Replacing country with exact sender and
receiver BIC raises it sharply to **0.6609**; adding UTC hour-of-week changes little
(**0.6612**), while a smoothed exact directed-pair residual reaches **0.7047**.
July log RMSE falls1.994→1.189→1.110. Pair effects cover2,661,260 July rows from
1,079,912 earlier observed pair cells; unseen pairs fall back to endpoint effects.

The effects are exceptionally stable across periods among well-populated cells. Earlier
versus July log-residual correlations are **0.99947** for1,105 sender BICs,
**0.99946** for925 receiver BICs (at least500 rows each period), and **0.98742** for
2,448 directed pairs (at least100 rows each period). Candidate construction: draw
duration from a multiplicative/mixture distribution whose location depends strongly
on the two endpoint banks, with a smaller corridor term after route stages. This is
predictive evidence, not proof of queues or SLAs. Median predictions still have large
seconds errors and the model does not identify the residual fast/slow mixture.

Evidence: independent `build_bank_cache.py`, `duration_currency_models.py`, actual logs,
model scores, stability table and manifest. The preserved failed log records pandas
interpreting country code `NA` as missing before `keep_default_na=False` fixed it.

## C-C3 · Alternative currencies come from a sender-country menu, not exact corridors

Earlier sender-country modal currency predicts **2,590,679/2,896,968 = 89.43%** of July.
The top two earlier currencies cover **94.80%** and the top three **96.77%**. Among rows
missed by the first sender-country choice, the second choice accounts for about50.9%
of misses and the third another18.6%. Exact sender BIC does not improve the score
(89.42%); directed-pair modes with minimum cell sizes5,20 or100 are equal or slightly
worse after falling back to sender BIC.

Receiver information does not explain the remaining choice in this modal test. On
sender-BIC misses, receiver-country mode is correct43.90%, slightly below the global
mode at44.06%; receiver-BIC is43.78%. Pair modes are only1.79% correct even with any
earlier pair history and approach zero in denser pairs. Candidate construction: select
currency from a stable sender-country-specific ranked distribution or small menu rather
than a deterministic home currency plus corridor override. Exact probabilities and
rare fourth-or-later choices still need a probabilistic likelihood review. Because
mode tests ignore probability calibration, this is a partial rule, not a complete sampler.

Evidence: `currency_model_scores.csv`, `alternative_currency_scores.csv` and the shared
duration/currency script/log. Complete-date and sparsity boundaries are explicit.
