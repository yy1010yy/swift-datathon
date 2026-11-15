# C independent initial: ordinary directed-pair recurrence

Population: full9,992,994 payments with no recorded anomaly label, exact raw account
text, all currencies, no deduplication. Full10M source scan and32 exact-string partition
groups completed. Results written before seeing another reviewer’s general-population
counterparty results. Count/interval methods and candidate challenges were pre-recorded
in `counterparty_method.md`.

## Exact population and count structure

There are8,258,480 observed directed pairs. Every observed pair has consistent party
types across its payments (zero MIXED pairs); this is pair consistency, not proof that
all account identities have globally consistent role labels. Eight adjacent equal-time
repeats are preserved. No account-text normalization was attempted.

| Party | Observed pairs | Payments | Repeated pairs | Maximum payments/pair |
|---|---:|---:|---:|---:|
| BB |1,859,443|2,269,885|147,796|936|
| BC |4,520,169|5,600,965|383,532|2,310|
| CB |544,151|609,762|26,714|488|
| CC |1,334,717|1,512,382|70,536|475|

Most pairs appear once, while a small tail repeats hundreds/thousands of times. A
single homogeneous count rate within each party category does not explain this spread.
For example BB full has1,711,647 singletons (92.05% of observed pairs), while a positive
geometric fit matched to its observed mean predicts81.92%. Simple zero-truncated
Poisson and positive geometric fits produce large discrepancies in each party/period
group (`counterparty_count_models.csv`), including recurrence far beyond these simple
families’ tails. These are negative family checks; the exact alternative generator is
not identified.

Business-sender pair repetition is descriptively more common (BB7.95%,BC8.48%) than
consumer-sender pair repetition (CB4.91%,CC5.28%), with the direction repeated in early
and July windows. This is an observed-pair fraction, not a per-payment partner-choice
probability or a causal customer-type effect. Account activity, corridor mix, latent
relationships and synthetic entity populations remain alternative explanations.

## Intervals and observation-window limits

Strict-past intervals are available for1,734,514 rows. Early median gaps range roughly
5.5–6.8days across the four party groups; July medians roughly13.1–16.0days. Fitting a
single exponential waiting family to early gaps gives poor July predictions. This does
not establish that actual payment habits slowed: earlier payments have less visible
history, first occurrences are censored, and July includes across-boundary gaps. The
observed pair cohorts differ greatly; for example only210,005 of3,300,701 early BC
pairs recur in July, while1,219,468 July BC pairs are newly observed.

No fixed weekly/monthly recurrence rule has been reconstructed. A heterogeneous
relationship/activity mechanism is a plausible next model, with matched-degree/corridor
and full exposure/risk-set checks needed before interpreting causal business schedules.
A highly active sender or popular receiver alone can create many repeated edges; count
tails do not by themselves establish pair-specific affinity. A next distinguishing test
would compare observed pair counts to sender/receiver-volume-preserving permutations.

## Contrast to special processes

ROMANCE uses500 dedicated pairs with2–8 labelled records and short minute-scale
growth sequences; these are excluded from the ordinary count population. Their typical
minutes-scale lags are unlike pooled ordinary observed repeat gaps. Duplicate-labelled
exact replays are also excluded from blank-label baseline; ordinary repeats are retained
and never assumed erroneous. Anomaly comparisons require suitable matched controls,
not simply replacing their denominators with the8.26M ordinary pairs.

## Evidence and limits

`counterparty_population.py`, actual `counterparty_population.log`, count histograms,
model cells, period/cohort summaries, interval summaries and complete manifest. Ignored
disk partitions retain all selected raw account text; full pair summary and interval
arrays permit independent implementations. Hashes choose shards only, never identity.
No zero-transfer pair universe or external economic data is assumed. The redundant
interval-denominator assertion passed in `counterparty_population_verify.log`: exactly
8,258,480 first-timestamp rows lack prior history and1,734,514 have it, summing to
all9,992,994 blank rows. All eight timestamp ties occur later within a pair. Findings
remain provisional until independent review/debate/lead verification.
