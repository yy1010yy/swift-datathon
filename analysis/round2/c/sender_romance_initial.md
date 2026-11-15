# C independent sender-history and romance initial results

Saved after C's third full-file scan and before seeing A/B's sender-history or
romance computations. All 10M rows scanned again; exact account-text sender matches.
No external country, economy or label information was used.

## Sender-history checks

The broader same-sender/currency histories contain prior records for 603/649 account-
replacement cases. Only eight repeat a previous amount paid to a different beneficiary;
none repeats the same beneficiary. Nearest earlier unlabelled same-sender/currency
controls have 12/591 history-eligible exact-different-beneficiary repeats. This does
not support recovering invoice replacement by this simple amount-matching test.

Fat-finger: exact powers of ten relative to any earlier same-sender/currency amount
occur in 23/1,788 history-eligible targets, versus 32/1,723 matched eligible controls.
Recall has six different-beneficiary exact repeats among 301 eligible targets versus
12/293 eligible controls. These tests do not reconstruct either label mechanism.
The original intended invoice may be absent; account formatting, altered currency,
different amounts and truncated observation windows remain possible limits.

Controls are the latest earlier unlabelled observation for the same sender/currency.
They may be reused for several targets; they are not statistically independent or
randomized. Each control itself is scored using strictly earlier records. Files:
`sender_summary.csv`, `sender_controls_summary.csv`, `sender_tests.csv`,
`sender_controls.csv`; actual outputs in `sender_run.log`, `sender_controls.log`.

## ROMANCE_SCAM: rapid, usually growing payments

Among 2,476 labelled romance records, 1,973 have strictly earlier same-pair/currency
history. The latest preceding-payment gap ranges 1–2,192 seconds; mean 306.95,
SD 301.32, median 215. The next/latest-prior amount ratio has median 1.5;
1,639/1,973 increase, 323 decrease and 11 are equal. Natural-log ratio mean is
0.4030 and SD 0.4103. These are compatible with a rapid series using exponentially
distributed waits around 300 seconds and lognormal multiplicative growth centered
near exp(0.4), rather than a deterministic 50% increase.

Retrospective stability: pre-July n=1,349, mean wait313.55s, median217s, median
ratio1.5; July n=624, mean wait292.69s, median212s, median ratio1.4935.
The 503 without observed prior history could include starts or incomplete histories;
they are not automatically 503 independent sequences. The precise distribution and
causal construction remain provisional until independent review and fit comparisons.

Strongest alternatives: ordinary repeated payments in selected pairs, overlapping
series, differing histories and ordering effects. Earlier timestamps establish temporal
precedence, but not intention. Need independent lag/log-ratio calculations, prior-label
composition, and predictive distribution checks; same-currency raw account-text matching
may miss equivalent representations. Source: `romance_history_cases.csv` and core raw
history extract `relevant_pair_history.csv.gz`.

## Power-of-ten method correction

Initial core method tested only the exponent nearest log10(amount ratio), with ±1
target-cent tolerance. Independent review correctly noted that tiny amounts can
satisfy more than one exponent under that broad tolerance. `power_sensitivity.py`
enumerates all powers -6..-1 and1..6 using integer arithmetic. Exact shifts are now
the primary test; ±1targetcent and round-after-transform are separate sensitivities.
Within the same pair: FAT exact0/313, ±1cent3; romance exact0/1,973, ±1cent3
(initial nearest-power method found only one). Controls exact83/14,788, ±1cent548.
Both versions and the correction remain available; no primary duplicate counts changed.
