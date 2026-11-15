# B independent population counterparty initial

Saved before reading C counterparty conclusions. Independently regrouped all32shared
raw-record partitions, comparing full sender/receiver strings and independently joining
strictly preceding distinct timestamps. Shared extraction is disclosed: C filtered the
source into raw partitions; B reimplemented identity grouping, count models and histories.

All9,992,994no-recorded-label payments form8,258,480exact directed pairs. None has
mixedB/Croletypes.7,629,902pairs appear once;628,578appear more thanonce. Those
recurringpairs contain2,363,092payments; the number of payments after eachpair'sfirst
observation is1,734,514. These units differ and must not be interchanged. Eightextra
same-timestamp rows remain within later timestamp batches; every pair has one first
timestamp row lacking observedhistory. Exactstring identity is not necessarily a
stable bank-qualified realcustomer identity.

## Simple count distributions fail even within party groups

Full-window means perobservedpair areBB1.22073,BC1.23911,CB1.12057,CC1.13311;
maximum payments936,2310,488,475respectively. Fit positivegeometric and zero-truncated
Poisson separately per role/period, without inventing a zero-paymentpair population.
ForBBfull, binnedTV errors are.11322geometric/.12810Poisson; BCfull.12044/.13763.
Large singleton mass and a long repeat tail remain, so one homogeneous countfamily
does not recover the edge-generation mechanism. This is a negative result; heterogeneous
customer activity, popularity, schedules and selection are plausible but unproved.

## Homogeneous exponential waiting also misses structure

Earlier-role mean positive wait is approximately895777sBB,888042sBC,996599sCB,
968606sCC. OnJuly the earlier-fitted exponential's binnedTV errors are.16088,.16048,
.15346,.14946respectively. Histograms/quantiles and all8role/period fits are saved.
The latest-prior timestamp is strictly earlier; same-time payments never create a zero
wait, and July events can refer to earlier-period predecessors.

Finite-window boundaries matter: first observations have no known past, long waits
are less likely to be observed before the dataset ends, and the July pair cohort
differs from the earlier cohort. Counts are fitted separately byperiod; that is not
a forecast of pair growth. No-label filtering can omit a labeled intermediateevent.
No homogeneous-model failure proves one specific business purpose or generator.

Runtime231.26seconds on shared partitions. Evidence:counterparty_review.py,
counterparty_method.md,actualrunlog,count histogram/summary/models,interval summary/
models,cohorttable and counterparty_initial.json. Mainpopulation and denominator
controls pass9,992,994rows =8,258,480first-timestamp rows +1,734,514strictpriorrows.
