# Timing model debate and comparison boundaries

A independent extension supports lead/B's finding that sender-code UTC profiles are
needed beyond party mix. Lead hour-only scores predict24 hour categories and must
not be directly compared to A's168 hour-of-week scores; the target outcomes differ.
Lead conditional-hour population2,896,963 excludes five sparse training-absent strata;
A uses country/pooled fallbacks and scores all2,896,968 complete-date July rows.
These denominator differences should accompany reported scores rather than being
silently reconciled by rounding.

A's actual deciding comparison uses one common July population for all ownmodels:
separable sender-hour×globalweekday NLL4.89644, fullsender-partyweek168joint4.88143,
sender-only168template4.87652(alpha.5), sharedphaseweeklytemplate4.87488. This suggests
shared weekly schedule plus phase is a useful parsimonious mechanism, though the phase
model still needs independent parameter/prediction review before being called recovered.
One inferred phase cannot establish a timezone or real local business clock.

Perparty hour splitting fails to improveNLL; richer joint templates benefit from sharing
over party. Cyclic neighbor smoothing worsens NLL relative to unsmoothed templates,
consistent with sharp timing boundaries but not proof of their source. Alpha sensitivity
is shown completely; selected settings are retrospective development, not untouched tests.

Weekly-volume×weekday factorization nearly fits complete-week counts (TV.0029645)
but local cells differ up to about10%. The13 near-.005 shares are exploratory: finite
counts, UTC first/last-week boundary leakage and sender composition challenge exact
quantization. The country/week and party/week tables retain those objections. No
external dates, holidays, GDP, country populations or timezone tables enter this work.
