# Independent C — anomaly histories and amount distributions

Questions fixed before reading other reviewers' results:

1. Does DUPLICATE_PAYMENT repeat a strictly earlier transfer of the same USD amount,
   currency and exact directed account pair? Is its repeat fraction higher than that
   of unlabelled payments in the same selected pairs?
2. Does FAT_FINGER_MISTAKE differ by a power of ten from a strictly earlier amount
   for that same directed pair and currency? Report missing histories separately.
3. Do CUSTOMER_RECALL and scam labels show these signatures, or only label/party-type
   restrictions? A label name does not prove the mechanism.
4. Within currency and B→B/B→C/C→B/C→C, are amount distribution scales different,
   and do patterns persist in July compared with pre-July records?

Candidate mechanisms: accidental replay, decimal-place error, party-type-constrained
fraud injection, and conditional amount sampling. Competing explanations: legitimate
repeated invoices/regular payments, chance amount coincidences, account-format changes,
and differing population/currency mix. Missing prior history cannot falsify an injected
mechanism that refers to a record outside the observation window.

`anomaly_amount.py` reads every cleaned row twice, using CSV-aware chunk parsing.
First pass keeps all 7,006 labels, measures label×party composition, and calculates
exact quantiles/log moments by currency×party×period×labelled indicator. All amounts
are retained; no random sample or tail removal. Pre-July means timestamp strictly
before 2023-07-01 00:00:00 UTC; July is the later period, not a pristine holdout.

Second pass keeps every row whose exact raw account-text pair occurs in a labelled
record. Account identifiers remain text, including spaces and punctuation. Currency
must also match for the prior comparison. Each row sees only strictly earlier Unix
timestamps; same-time records do not count as history even if physically earlier.
File order is not used to establish temporal precedence.

USD source amounts are parsed to rounded integer cents. Decimal-shift tests use nonzero
integer powers of ten from -6 through +6, allowing one cent rounding. This deliberately
tests a broad family; a match alone is not proof of error. Unlabelled controls share
the selected pairs but are not randomly sampled from the full population and may
have different history depth. Report both all-row and known-history denominators.
Pair history comparisons use exact account strings, not reconstructed normalized IDs;
formatting changes could make observed histories incomplete.

Saved code, `run.log`, CSV tables, row-level evidence and manifest capture this
independent execution. Labelled and history extracts contain synthetic identifiers;
retain the original dataset disclaimer when sharing. No claim is reviewed/final until
the lead compares independent results, exchanges the debate and resolves challenges.

## Later targeted tests and cache location

`sender_history.py` scans the full10M rows a third time and extracts histories for
labelled senders. Its87MB compressed raw-derived cache is now stored under ignored
`outputs/round2/c/sender_history.csv.gz`; both sender scripts use this location.
No rescan was needed to move it. Small test cases and tables remain here. Run
`sender_controls.py` after sender extraction to reproduce nearest-earlier-unlabelled
same-sender/currency controls. Control rows can repeat across targets.

`power_sensitivity.py` supersedes the initial nearest-exponent heuristic: exact
integer-cent equality after powers -6..-1,1..6 is primary; exhaustive ±1targetcent
and explicit round-after-transform are separate sensitivity results. Originals remain.
`romance_fit.py` uses greatest numeric source record among tied latest prior timestamps;
the initial smallest-source version is preserved. Ties have no observed actual order.

`amount_model.py` fits exact OLS using C's full-file log-moment sufficient statistics;
`compare_amount_models.py` independently verifies B's raw-numeric fit. `fat_latent.py`
fits exploratory latent-shift mixtures to currency/party-adjusted FAT log amounts,
using the early baseline and evaluating July. This does not recover individual intended
amounts; unchanged or broad mixtures remain alternatives requiring independent review.
