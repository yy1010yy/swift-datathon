# B independent timing-model initial

Own full-source timing_counts.csv, completeMay1–June30discovery andJuly1–30evaluation.
Initial script and results were computed before receiving A/lead timing scores; this
prose records them after the exchange. Full training/timing rows are in the manifest.
Condition on each observedJuly sendercountrycode/party total, so changing sendermix
cannot alone explain improvements. No external timezone mapping or localhours claimed.

The exposure-aware uniformcalendarbaseline hasJulynegative loglikelihood5.16121.
Pooled weekday×hour jointtable5.01885; sendercode/party fullweekday×hour4.88095.
The simpler factorized sendercode/party model withhourprofileandweekendweekdayrate
scores4.89986; distinguishing allsevenweekdayrates improves4.89449. Fulljointstill
improves.01355nats/record overfactorizedweekday/hour, suggesting weekday-hourcoupling
not captured byone commonmultiplicativehourschedule. FulljointweightedconditionalTV
is.05884versus.07617forfactorizedsevenweekday/hour and.08363forweekend/hour.

Allmodels see same2,896,968Julyrecords. Fiveoccur in sendercode/partycombinations
unseenbeforeJuly and useglobalsmoothing. Conditionaltables get168pseudocounts toward
theglobalearliercountdistribution, fixedbeforeviewingJulyscores. Allweekdayexposures
are explicit:MayJune9days eachMon–Fri and8eachSat/Sun;July4eachMon–Fri and5eachSat/Sun.
Logloss/TV are descriptivepopulationfits, not iidcausaltests. These areUTCclockpatterns,
not uniquely recoveredlocalschedules orcustomerpreferences.

Question for next extension: doesa circular168-hour sharedschedule withcode-specific
phase accountforthecoupling moreparsimoniously? Can13completeweeksfactorize daily
volume into weekamplitude×weekdayrate? The savedtimingtablehasperiodaggregatesonly,
so latterrequires theexistingfullnumeric timestampcache, not anewrawscan.
