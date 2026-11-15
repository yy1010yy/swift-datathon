# General counterparty recurrence — independent C method

Question: outside recorded anomaly labels, how often does the same exact directed
account pair recur, and can a single simple count/arrival family explain its variation
within each customer-type pair? Do early/July summaries preserve the same pattern?

Population is all9,992,994 blank-label payments. Blank means no recorded label, not
proven legitimate. Do not use the earlier labelled-pair extract as a population sample.
Exact raw account text defines identity; no punctuation removal or inferred account
normalization. Different representations of the same underlying account could therefore
remain separate. All currencies are pooled for this directed-edge question.

`counterparty_population.py` partitions the full file into32 disk files by a stable
sender hash. Hashing only routes records to files; complete raw sender/receiver strings
are retained and compared, so a hash collision does not merge different pairs. Each
partition is sorted and grouped independently. This avoids a full10M-string in-memory
table and preserves quoted CSV parsing. Original inputs are untouched.

Per-pair outputs include full/early/July counts and first/last observation. Early is
before July1UTC, July is thereafter. A pair with inconsistent business/consumer types
is explicitly marked MIXED instead of silently assigned to a role. Count-family fits
use only observed pairs; zero-transfer potential pairs and their population are unknown.
Do not interpret an observed-pair distribution as a population contact probability.

Inter-arrival gaps use the latest *strictly earlier distinct timestamp* in that pair.
All first-timestamp rows lack observed history; tied later rows share the earlier
distinct timestamp. The separate adjacent-time zero count preserves simultaneous-event
evidence. Period assignment uses the later payment, including pre-July→July transitions;
it does not discard history at the July boundary.

Candidates: a homogeneous zero-truncated Poisson count or positive geometric count;
an exponential waiting-time family fit to early positive gaps and compared with July.
Alternatives: heavy degree/usage mixtures, scheduled bills/payroll, bursty shopping,
calendar-dependent activity, account formatting and finite observation censoring.
Counts are fitted separately by period because exposures and observed-pair cohorts
differ. Fit failures are informative negative results, not proof of one alternative.

Exact counts and interval arrays are retained. Small summary/model-cell tables stay
under `analysis/round2/c`; disk partitions, complete pair summaries and interval arrays
are ignored `outputs/round2/c/counterparty_population/`. Reproduce with:

```
.venv/Scripts/python.exe analysis/round2/c/counterparty_population.py
```

The scan refuses to append to existing partitions. To reuse a completed scan and
rerun postprocessing, use `--phase analyze`. Both phases must complete and write
`counterparty_manifest.json` before claiming a finished full-population result.
The task remains provisional until independent comparison/debate and lead verification.
