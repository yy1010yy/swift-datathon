# Round 3 A — independent questions and challenges

Saved before reading any other round-3 result.

## B1 · Exact-bank and corridor effects

Question: after preserving currency, customer type, route, participant count and FX
controls, do exact sending/receiving BICs or directed BIC pairs predict July currency,
amount, Covered choice, UTC week-hour and duration better than country-level models?
Fit on records before 2023-07-01 UTC and score July. Exact-pair results use a stable
1/64 BIC-pair sample retaining all occurrences, because millions of sparse pairs would
otherwise turn memorisation into apparent accuracy.

Candidate rule: country selects a broad regime, then exact banks/corridors add stable
preferences. Business meaning: bank products and correspondent relationships constrain
currency, route and processing. Competing explanation: exact-bank gains are sparse-cell
overfit or merely proxy volume/currency mix. A later-period improvement with smoothing
and explicit fallbacks supports a stable bank effect; failure outside large cells or no
gain over country challenges it.

## N1 · Entity activity, pair affinity and correspondent topology

Question: can sender/receiver activity alone explain repeated directed account pairs,
and how predictable is the first intermediary from the sending bank/currency? Compare
observed repeat fractions with a transaction-volume independence model, using a stable
receiver-account sample with complete pair histories. Separately compare country- versus
exact-bank prediction of the first visible intermediary on continuous non-Direct paths.

Candidate rule: heterogeneous account activity creates much of the degree tail, while
durable pair affinity creates excess repetition; intermediaries are drawn from bank-
and-currency-specific correspondent pools. Competing explanations include finite-window
censoring, account reuse across BICs, endpoint perturbations and sparse categories.
Evidence for affinity requires observed repeats exceeding the activity-only conditional
expectation; evidence for bank-specific pools requires later-period prediction beyond
country/currency. Neither test proves a real customer relationship or legal bank network.
