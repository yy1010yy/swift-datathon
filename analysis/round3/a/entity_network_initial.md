# A independent initial — entity activity and pair formation

Saved before seeing any other round-3 result. Code and actual output:
`entity_network.py`, `entity_network_manifest.json`, `activity_null_summary.csv`,
`activity_null_cells.csv` and compressed endpoint-activity summaries.

## Population and units

The input is C's completed exact-string pair extraction of all **9,992,994** payments
with no recorded anomaly label, containing **8,258,480** observed directed pairs. I
independently regrouped the pair summary for all 390,725 ordering accounts. Receiver
tests use a deterministic 1/64 sample of exact beneficiary-account strings, retaining
every pair/payment of 40,392 selected receivers: 126,138 pairs and 151,383 payments.
This independently scores pair formation but shares C's raw blank-label extraction.

## Initial conclusion

Account activity is extremely heterogeneous and largely determines degree. Ordering
accounts have median3 payments but p99=404 and maximum75,773; median observed receiver
degree3, p99=324, maximum38,394. Correlation between log payments and log degree is
**0.9963**. In the sampled beneficiary population, median activity/degree are1/1,
p99=36/29 and maxima7,728/4,558; log correlation **0.9520**. Thus a generator with
heterogeneous endpoint activity is necessary and explains much of the degree tail.

Activity alone is insufficient. Under a bipartite transaction-volume independence
challenge, pair `(i,j)` has Poisson mean `sender_volume_i × receiver_volume_j / N`.
Conditioning on the pair being observed gives an expected repeat probability. Actual
repeat fractions exceed that expectation in every party group:

| Party | Observed repeat share | Activity-only expected | Observed / expected |
|---|---:|---:|---:|
| BB | 7.12% | 1.54% | 4.62× |
| BC | 9.10% | 2.71% | 3.36× |
| CB | 4.03% | 0.55% | 7.31× |
| CC | 5.38% | 0.99% | 5.42× |

Excess repetition also appears in fixed log2 activity cells, including cells with
hundreds of pairs where the independence expectation is near zero. This challenges an
explanation based only on popular receivers and active senders. A candidate construction
is: draw heterogeneous account activity/popularity, then add relationship-specific
affinity or recurring schedules that make an already chosen pair more likely to repeat.

## Strongest challenge and boundary

The activity null is a deliberately simple configuration-style model, not the best
possible degree-preserving generator. Finite-window censoring, corridor restrictions,
currency compatibility, account reuse across BICs and latent customer segments can all
create excess pair repetition without a literal pair-affinity parameter. Pair identities
are exact synthetic strings, not proven people. Therefore the supported conclusion is
that **endpoint activity alone does not reproduce ordinary recurrence**; the test does
not choose among relationship affinity, schedules and additional shared constraints.
