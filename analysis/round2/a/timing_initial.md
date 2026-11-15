# Independent A timing models

Pre-analysis questions are saved in `timing_question.md`. Shared raw contingency
extraction is B's all-file `timing_counts.csv`; modeling is independently implemented.
Train uses May1–June30 complete UTC dates; test July1–30 includes2,896,968 payments.
Weekday calendar exposures are [9,9,9,9,9,8,8] early and[4,4,4,4,4,5,5] July.
No July sender code is unseen. Smoothing adds0.5 per hour/day/joint cell.

Within each observed July sender-code/party group, predict the hour×weekday probability
distribution. This conditions away changes in sender/party composition. July mean NLL:
uniform5.161209; weekendmultiplier×pooledhour5.029650; separateweekday×pooledhour5.026160;
sendercodehour×pooledweekday4.896442; sendercodepartyhour4.897142;
sendercodehour×sendercodeday4.893767; jointsendercodepartyhourweekday4.881434.

Thus sender-specific UTC hour shape is a material scheduling component. Splitting
hour profiles further byparty does not improve logscore here; sparse-cell overfitting
is a competing explanation for its slight worsening. A global weekday multiplier and
hour profile is inadequate. Even country-specific separable profiles leave interactions;
joint models perform better, but their richer parameter count and smoothing matter.
These are explicit probabilistic time-generation candidates, not customer-local clocks.

Pooled exposure-corrected early weekend/weekday rate ratio=.307948. Saturday33932.75
payments/day versus Sunday53585/day; weekdaymax/min=1.07672. A single uniform
weekday/weekend multiplier misses asymmetry. Timezone-shifted activity, sender-code mix
and day-specific generators are alternatives; no external timezone/economic data used.

Exact scores, per-group scores, calendar rates and sender hour profiles are saved in
`timing_model_scores.csv`, `timing_model_strata.csv`, `timing_exposure_rates.csv`,
`timing_sender_hour_profiles.csv`; actual execution log `timing_initial.log`.
Further mechanism work could infer circular weekly phase shifts from payments alone,
then test whether a shared activity template predictsJuly without full joint tables.
