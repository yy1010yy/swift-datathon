# Round 3 C independent question register

Saved before reading any A/B round-3 result. Evidence is limited to supplied rows.

## C-A1 · Remaining anomaly mechanisms

- **Question:** For CEO, account-replacement and recall labels, which strictly prior
  same-sender/currency features distinguish the target from its nearest earlier
  blank-label control?
- **Population:** All 945 CEO, 649 replacement and 317 recall rows, exact raw accounts;
  histories use timestamp `< target`, never file order. Controls already selected in
  round 2 and are rescored with only their own earlier history.
- **Measures:** recipient account/BIC novelty, prior same-BIC/different-account history,
  prior same-pair history, amount percentile/ratio, sender-bank novelty and lag.
- **Candidate rules:** CEO chooses a new recipient for a business sender and atypical
  amount; replacement swaps the account while retaining recipient bank/corridor;
  recall refers to a recent earlier transfer.
- **Competing explanation/challenge:** the label may be injected independently after
  generating an ordinary payment; selected controls have shallower histories and are
  not randomized. Failure of enrichment is useful negative evidence, not proof that
  the documented concept is absent.

## C-D3 · Bank/corridor duration mechanism

- **Question:** After route, participant and FX controls, do exact sender/receiver BIC,
  directed bank pair or UTC hour-of-week materially improve later-period duration?
- **Population:** May 1–June 30 UTC training and July 1–30 evaluation; duration seconds,
  all rows on complete dates.
- **Measures:** July log-duration RMSE/R² and absolute error for fixed earlier-fitted
  hierarchical target-encoding models.
- **Candidate rule:** duration combines route stages with bank/corridor processing and
  weekly queue/service modes.
- **Challenge:** bank IDs can proxy currency, country or composition; predictive gains
  do not establish operational causality, and a mean model cannot identify mixtures.

## C-C3 · Alternative-currency choice

- **Question:** When a payment does not use the sender code's usual currency, can exact
  sender BIC, receiver BIC or directed bank pair predict the alternative?
- **Population:** same complete-date May–June training and July evaluation.
- **Measures:** top-1/top-2 accuracy, coverage, and accuracy within sender-mode misses;
  sparse pairs fall back to sender BIC/country.
- **Candidate rule:** a sender has a small preferred currency menu, adjusted by receiver
  or corridor.
- **Challenge:** exact pair modes can overfit rare cells; minimum training counts and
  fallback coverage must accompany every score.
