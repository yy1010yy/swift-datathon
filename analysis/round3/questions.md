# Round 3 question and theory register

## B3 · Exact bank and corridor rules

- **Question:** On July payments, how much do exact ordering BIC, beneficiary BIC and
  directed BIC pair improve prediction of currency, amount residual, Covered choice,
  UTC time and duration beyond sender/receiver country, party type, route, participants
  and FX?
- **Population:** all rows for descriptive models; blank-label rows for ordinary amount
  and duration sensitivity; non-Direct rows for Covered choice. Fit before July and
  score July. Preserve sparse/unseen cells with explicit fallback.
- **Measures:** log loss for categorical outcomes; log-amount/duration RMSE or likelihood;
  weighted calibration and coverage; number of seen/unseen BICs and corridors.
- **Candidate rule:** the generator assigns stable bank or corridor profiles that
  influence several downstream fields.
- **Business theory:** institutions and correspondent relationships have preferred
  currencies, operating schedules, routing practices and service speeds.
- **Competing explanation:** exact BIC merely encodes country, currency zone, customer
  mix or high-dimensional overfit.
- **Challenge:** no later-period improvement after lower-dimensional controls, or gains
  restricted to rare cells.

## N3 · Entity and correspondent-network formation

- **Question:** Can sender activity, receiver popularity, bank/currency corridor and
  degree explain pair recurrence and intermediate-BIC selection, or is a relationship-
  specific component still required?
- **Population:** blank-label account edges for ordinary recurrence; all visible route
  BICs for correspondent selection, with gaps retained but not interpreted as banks.
- **Measures:** account/bank activity and degree distributions; repeated-edge excess
  versus activity-preserving expectations; later-period prediction of known pairs;
  conditional intermediary-choice concentration and unseen rates.
- **Candidate rule:** draw heterogeneous entity activity/popularity, then add persistent
  pair affinities and currency/corridor-specific correspondent pools.
- **Business theory:** frequent customers, popular beneficiaries and established banking
  relationships generate concentrated flows through preferred hubs.
- **Competing explanation:** apparent pair affinity is fully induced by marginal degrees
  and finite-window exposure.
- **Challenge:** an activity/degree-only model reproduces repeat counts and conditional
  intermediate choices without pair-specific information.

## A6 · Remaining anomaly mechanisms

- **Question:** Do CEO, account-replacement and recall labels have recoverable strictly
  earlier signatures in account, beneficiary, bank, details, amount, currency or time?
- **Population:** every row with the three labels, plus comparable strictly earlier
  blank-label controls selected without future information. Report missing history.
- **Measures:** exact/near amount reuse, changed beneficiary/account/BIC with stable
  sender or detail signature, lag distributions, possible reverse/recalled transfers,
  and enrichment over controls.
- **Candidate rules:** CEO redirects a business sender to an unusual beneficiary;
  replacement changes account details while retaining invoice-like amount/context;
  recall refers to an earlier customer payment.
- **Competing explanation:** labels were injected from latent intended payments or
  metadata absent from the file, leaving no visible predecessor signature.
- **Challenge:** target signatures are no more common than matched blanks or depend on
  post-event information.

## D3/C3 · Duration regimes and alternative currency

- **Question:** Do exact banks/corridors, UTC schedule and latent service regimes explain
  duration beyond route/participants/FX? For payments not using the sender's earlier
  modal currency, which receiver/corridor/party/route/amount features predict the choice?
- **Population:** fit on pre-July rows and score July; report unseen cells. Repeat duration
  on blank-label and continuous-path populations.
- **Measures:** held-period likelihood/RMSE/MAE and calibration; conditional quantiles;
  categorical log loss/top-k accuracy for currency.
- **Candidate rule:** banks/corridors select processing regimes and a small currency menu;
  alternative choice depends on the receiver/corridor and payment context.
- **Business theory:** service channels, cut-offs and correspondent arrangements create
  fast/slow duration modes; corridor demand drives non-home-currency payments.
- **Competing explanation:** improvements arise from sparse memorization or time-varying
  composition rather than stable operational rules.
- **Challenge:** exact-bank models fail July, or simple country/route baselines perform
  equally well after smoothing and unseen fallbacks.

