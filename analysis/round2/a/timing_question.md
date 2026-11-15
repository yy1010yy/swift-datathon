# Timing independent pre-analysis question

Before inspecting model results: using B's full-population exact timing contingency
table only, can a separable model (weekday-specific daily rate × hour distribution)
predict July timing within sender-country-like-code/party strata? Does allowing
sender-specific hour shape improve over a pooled hour shape, and do party-specific
profiles add further predictive value? A simple weekend multiplier may leave weekday
asymmetry unresolved. This is a statistical scheduling mechanism, not local time inferred
from external geography.

Train on complete May1–June30 UTC dates; evaluate complete July1–30 only. Count actual
calendar exposures for each weekday in both periods. Do not compare raw weekday
counts without dividing by exposure. Predict conditional distributions within observed
July sender-code/party strata so changing population mix cannot alone explain gains.
Use small positive smoothing to prevent empty training cells giving infinite scores;
report train-absent codes and sensitivity. Compare uniform timing, pooled hour/day,
country-hour and country-party-hour models, plus joint hour×weekday alternative.

Deliver exact model scores and rate/profile tables, sparse-cell coverage, variation
boundaries, and retained negative results. B table is shared extraction; independent
modeling does not constitute a second independent raw-data scan.
