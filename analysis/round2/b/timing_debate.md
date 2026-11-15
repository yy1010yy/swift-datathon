# B timing debate and mechanistic extensions

Independent B primary counts/model execution preceded exchanged A/lead scores;
timing_initial.md discloses prose timing. A/lead independently confirm sendercode
profiles explain UTC timing much better than one pooled profile, and customerrole
adds little after countrycode. Scores with different conditioning (hour-only versus
fullweekhour) have different normalizers; compare within each implementation.

## Deciding comparisons on the same July population

B holds each observedJuly sendercode/party total fixed, avoiding sender-mix changes
as the sole explanation. CompleteMay1–June30train andJuly1–30test,2,896,968testrows:

| Earlier-fit model | July negative loglikelihood | Weighted conditional TV |
|---|---:|---:|
| Calendar-exposure-aware uniform |5.161209|.342464|
| Pooled weekday×hour joint |5.018853|.216015|
| Party-only weekday×hour joint |5.018734|.215938|
| Sendercode fullweekday×hour |4.876509|.055097|
| Sendercode/party fullweekday×hour |4.880946|.058837|
| Sendercode/party factorized weekday×hour |4.894493|.076168|
| Sendercode/party weekendfactor×hour |4.899861|.083634|
| One common168h circularprofile + sendercodephase |4.874931|.054704|

Thus a commonhourschedule times a weekday/weekend factor leaves meaningful residuals.
Code-specific circularphase of a commonweeklyshape is a compact mechanistic candidate:
it performs slightly better than unrestricted sendercode tables, while extra party
stratification slightly worsens testfit. A's codehour+pooledweekday score4.89644points
in the same direction: weekhourcoupling matters beyond independent hour/day factors.

Circularmodel phases can be any0…167hours, jointly fitted with one template over30
alternatingiterations. They are arbitrary relativeweeklyphases, **not identified local
timezones**. A commonrotation of template/phases gives identical predictions, and
localoptima/sparsecodeoverfit are possible. No actualworkinghours,timezonecountrymap
or customerlocalweekdaycausality is proved. FiveJulyrows have code/partystrata unseen
in earliercounts; globalsmoothing handles them. Counterparty/currency/bank selection
could mediate the sourcecode association.

## Week-volume factorization

The period-aggregate timingtable lacksweekindices, so use B's fullnumeric timestampcache
without a newrawscan. May1–July30is exactly13completeweeks,9,991,528rows. A rowtotal×
columntotal rank1 model (weekvolume×weekdayrate) hasTV.0029645,RMSrelativeerror.01848,
maxcellrelativeerror.10366. Weeklyvolume therefore changes sharply while weekday
composition remains approximatelystable. This is all-perioddescriptive factorization,
not a forecast of Julyvolume from MayJune.

Weeklytotals cluster near50,000multiples; a possible discreteweekweight source is
exploratory. UTCboundaryspillover and codephase differences are alternatives. Preserve
observedcounts rather than asserting an exactquota or fixedrandomweightdraw.

Evidence:timing_models.py,timing_extension.py,actualrunlogs,modelscoreCSV,168htemplate,
phase/stratumtables,91dayfactorizationcells and timing_extension.json. Earlierweekend
ratio differenceMayJune~.31versusJuly~.33should be interpreted alongside changing
weekvolumes, day-hourcoupling and UTCphase, not a universalweekendprobability.
