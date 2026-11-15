# B/C ordinary-counterparty review

B first saved counterparty_initial.md from independent full regrouping of C's raw
partitions; then read C counterparty_initial.md. All count/interval denominators,
party-specific count histograms and cohort structure agree. Shared source extraction
is explicit; B did not independently rescan the originalCSV for this task.

The strongest challenge to a homogeneous count model is the combination of many
one-time pairs and a very long repeat tail within the same party group. For example,
BB has1,711,647singletons among1,859,443observedpairs (about92.05%), whereas its
mean-fitted positive-geometric predicts81.92%. B independently fits both positive-
geometric and zero-truncated Poisson families and finds substantial binnedTV errors
even after role/period stratification. Observed maxima936BB/2310BC are incompatible
with treating a mean near1.2as a sufficient homogeneous count description. It does
not identify a particular heterogeneous alternative or prove pair-specific affinity.

The strongest challenge to a causal recurrence interpretation is observation-window
selection. A pair first appearing late has little exposure to recur; the observed
nonzero-pair universe and at-risk population differ byperiod. Early fitted exponential
waits predict July poorly (TVabout.15–.16), but July includes cross-period gaps and
different surviving/new pairs. This does not prove that customers slowed down, nor
does a long tail alone establish bills/payroll or regular monthly transfers.

Deciding comparison: exact full-identity regrouping, per-role/period count families,
strictly earlier distinct-timestamp histories, fixed earlier wait parameters evaluated
on July, and explicit early-only/both/July-new cohorts. Every count and history row
is preserved; zero-time adjacency is reported separately. Missing past and future
events, current observation length, filtered label events and raw identifier formatting
limit what can be reconstructed.

Final wording: **Most observed no-label account pairs appear once; a minority recur
often enough to create a long tail. A single homogeneous count or waiting-time family
within each party-type pair does not explain this pattern. A mixture of customer
activity, popularity, relationship persistence or schedules remains plausible, but
the precise repeat-payment rule has not been recovered.**

Keep8,258,480observedpairs,628,578recurringpairs,2,363,092payments inrecurringpairs,
and1,734,514strict-prior payments as distinct quantities. No absent-pair denominator
is supplied, so these are not probabilities that arbitrary customers transact. Role
pair consistency does not establish globally unique customer/account identity.

Verification:counterparty_verify.py,counterparty_verification.json and actual log.
Suggested next causal challenge is sender/receiver-volume-preserving permutations
or degree/corridor matched histories, with risk-set exposure handling; neither was
performed in this bounded test. Do not present that proposed next test as evidence.
