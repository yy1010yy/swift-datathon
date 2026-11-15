# B response after reading A: entity and correspondent-network formation

B's `initial.md` was saved first. Both A and B use C's completed blank-label pair
extraction but independently regroup exact account strings and score activity-only
benchmarks. Thus scoring is independent; raw filtering is shared.

## Exact population and differing benchmark samples

Both start from **9,992,994** blank-label payments, **8,258,480** observed directed
pairs and **390,725** senders. Full-sender activity controls agree exactly: median3,
p99=404, maximum75,773 payments; degree median3, p99=324, maximum38,394. A reports
log activity/degree correlation .9963. B additionally scans all2,589,757 receivers;
A uses a deterministic1/64 receiver sample (40,392 accounts,126,138 pairs).

The repeat expectations must therefore not be numerically merged. A's party ratios
(observed/expected 3.36–7.31) come from the receiver sample; B's full-population ratios
are3.55 BB,3.52 BC,5.59 CB,5.55 CC, with168,249 expected versus628,578 actual repeated
pairs overall (3.736×). Directions and magnitudes agree despite the different receiver
populations. Both independently reject endpoint activity/popularity as a sufficient
repeat mechanism.

Strongest alternative: the independence Poisson is deliberately simple. Currency and
corridor compatibility, finite-window exposure, latent customer segments and account
reuse can create excess repeat edges without a literal affinity draw. A degree-preserving
permutation with currency/corridor/exposure strata would better distinguish those causes.
The current justified rule is heterogeneous endpoint activity **plus another structured
relationship/corridor component**, not a uniquely identified affinity distribution.

Lead deciding check: reconcile B's full exact receiver totals against the pair summary;
recompute the conditional-Poisson result by party and selected activity bins; then run a
bounded degree/activity-preserving receiver permutation within party×currency/corridor
strata if the required fields can be joined without changing account identity. If not,
retain the current result as a strong negative test and state why the sharper comparison
is unavailable.

## Correspondent intermediaries

B separately tests all3,676,720 first-visible intermediaries. It finds a very unequal
but stable hub distribution (Gini.9339, top10 share19.21%, early/July TV.01743 and
correlation.99992 among active BICs). Earlier-fitted exact endpoints, sender currency
and exact BIC pair do not beat the global hub distribution in July; Indirect/Covered
marginals differ only modestly (TV.02675).

A's entity analysis does not inspect route internals, so it neither confirms nor
contradicts this result. The required second independent calculation remains missing.
Lead deciding check: independently extract every visible internal BIC position, compare
position-specific early/July distributions, and score global hub propensity versus
previous-BIC transition, route, currency and endpoint contexts. B's current first-position
result should remain provisional until that check. Even confirmation would support a
hub-weighted transition pool, not unconstrained global sampling or real-world centrality.
