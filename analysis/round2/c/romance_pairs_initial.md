# C independent romance-pair census

Calculated before seeing B's episode/pair findings. Population: all2,476 labelled
ROMANCE_SCAM rows, exact raw-text directed account pairs. Matching back to the
full-file pair-history extract recovers exactly2,476 rows, all ROMANCE_SCAM: there
are no unlabelled observed records in these pairs to act as same-pair controls.

- Exactly500 directed pairs.
- Every pair has a single payment currency;78 currencies across all pairs.
- Payment count per pair ranges2–8 inclusive. Frequencies:2→61pairs,3→95,
  4→64,5→71,6→74,7→66,8→69. This is compatible with discrete-uniform sequence
  lengths2..8, but does not prove that exact sampling program or exclude other families.
- Four pair/currency/timestamp cells contain tied labelled timestamps. Strictly earlier
  timestamp histories exclude ties;503 rows have no observed strictly earlier same-
  pair/currency record, versus500 pairs. The three-row difference is consistent with
  multiple first-timestamp records, to be explicitly verified rather than assumed.
- Therefore500 pairs can be treated as observed series for descriptive analysis;
  the file does not establish unobserved history or independent random seeding.

These constraints strengthen a candidate construction that injects dedicated short
consumer-sender payment series, rather than relabeling ordinary pre-existing pair
traffic. Without the generator code, alternative constructions remain possible.

Earlier C ratio-to-last calculations used first numeric source row among tied latest
prior timestamps. Lead/A/B use largest numeric source row, changing three of1,973
ratios but no lag or strict-history denominator. Treat this as tie-order sensitivity;
there is no observed temporal order among simultaneous records. Retain the first
version and use largest-source tie choice for the primary cross-review fit.
