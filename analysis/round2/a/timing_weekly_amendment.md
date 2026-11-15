# A independent weekly timing extension

Independent extension before receiving lead weekly results. Use shared B timing counts
for templates; week-volume information is lost from that period-collapsed table, so
recover exact thirteen complete weeks from shared B epoch/country/party raw cache.
No new independent raw-file scan is claimed.

## Weekly activity templates

A sender-specific168-hour rate template captures hour/day jointly. Fit MayJune and
reweight by July weekday calendar exposures. July2,896,968 conditional events score
NLL4.87652 with0.5 smoothing per cell, compared4.89644 for sender-hour×pooledweekday
and4.88143 for full sender-party-hour-weekday. The latter is more parameter-rich and
sparser; more detail is not automatically more predictive. Smoothing sensitivity:
alpha.1→NLL4.87712,1→4.87631,5→4.87662,20→4.88048,100→4.89767.
Cyclic neighbor smoothing worsens these scores; it may blur sharp schedule boundaries.
Sensitivity choices were inspected on July; do not label the selectedalpha untouched.

A parsimonious shared168-hour activity template with data-fitted sender-code integer
phase shifts (−24..24hours) reaches JulyNLL4.87488 after3 trainingiterations. This is
consistent with one weekly schedule shifted across sender codes, without importing
timezones or identifying customer-local clocks. Phase origin is arbitrary; alternative
latent schedules can yield similar fits. Exact templates, shifts and scores are saved.

The initial TV calculation included zero-weight countries absent fromJuly and produced
NaN. Initial log preserved as `timing_weekly_before_zero_weight_fix.log`; corrected
script excludes those zero-weight strata from weightedTV and reruns all calculations.
NLL values were unaffected. Do not present that failed diagnostic as a valid score.

## Weekly volume and weekday factorization

All9,991,528 payments from complete May1–July30 UTC dates form13 completeweeks.
Week-volume×weekday factorization has empirical total variation.0029645; individual
cell observed/expected ratios range.8963–1.0807. It is a close stochastic approximation,
not exact independence. Weekly observedshares lie near.005 increments, with maximum
absolute difference.0007499; this does not prove an exact discrete grid.

Country challenge:86 sender-code groups n>=10000 have weekly-shareTV versusglobal
.001625–.017281. Large sender groups show different first/last-week deviations.
Country composition, finite-count noise and UTC boundary shifts remain plausible
explanations. Inspect `timing_week_country_challenge.csv` and perparty shares rather
than treating13 near-grid points as unique evidence of a rounding rule.

Method/artifacts: `timing_weekly_extension.py` and actual log; weekly templates/scores,
phase shifts/template, exactweekcounts, week×dayfactorization and quantization tables;
`timing_week_challenge.py` and log/country/party tables. Retain full partial-day exclusions
and retrospective validation wording from the initial timing record.
