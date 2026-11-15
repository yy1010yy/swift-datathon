# A independent unified route-length initial

Computed from A's raw full10M route census before reading lead unified-route output.
Question: could participant length be drawn once as2+geometric failures, with Direct
defined exactly by length2, instead of choosing independent route category then length?

Early meanP2.581521 gives geometric success1/(meanP−1)=.6323026; actualDirectshare
.6322879. July meanP2.581696 gives.6322326; actualDirectshare.6324261. Direct iffP2
has0/10M exceptions. Fit early geometric law, retain expected/observed July length
cells including12+ tail. This unifies the length rules and is observationally equivalent
to flooring an exponential variate with matching rate. It cannot identify sampling
direction or the actual random-number call.

Covered among nonDirect has early probability.1132775. It is approximately constant
across participant lengths (15 early/July length cells n>=1000 have Pearson discrepancy
10.15). But adding FX strata strongly challenges a universal independent category draw:
44 period×length×FX cells have Pearson discrepancy2339.69 and covered shares.0972–.1605.
PooledFX0 coveredshare.157995 versusFX1 .106006 andFX2 .113844; counts are large.
Thus a length-only generator can fit the marginal but does not fully reconstruct
Covered vsIndirect assignment. Country/currency-zone and bank mix remain alternatives;
FX need not cause category choice. Small high-FX cells are not independently interpreted.

Artifacts: `route_unified.py`, `route_unified_initial.log`, `route_unified_fit.csv`,
`route_unified_length_cells.csv`, `route_unified_covered_cells.csv`. Earlier route-length
and gap-distribution fits remain supporting evidence, not replaced by source-code claims.
