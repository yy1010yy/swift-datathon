# Reviewer B pre-analysis questions

Independent full-population analysis before seeing reviewer A/C conclusions.
Data: all retained cleaned payment records; no external country/economic information.

## V2 · Payment-size construction

Question: within each payment currency, how do amount quantiles, log mean and log
standard deviation differ between BB, BC, CB and CC? Are these relationships stable
before July versus July? All amounts use normalized USD.

Proposed family: multiplicative customer-type/currency scales applied to a skewed base
distribution. Competing family: sender-type effects are only currency mix, or a few
anomalous tail records drive means. Compare conditional quantiles and log shapes, not
just means. Round-dollar counts test whether an additional rounding/salary-like mixture
is present. A stable median ratio does not identify an exact generator distribution.

## C2 · Currency construction

Question: within an internal sender/receiver BIC-country-code corridor, does currency
choice vary by customer-type pair and period? Counts retained for sparse combinations.
Country codes are positions 5–6 of the supplied BICs; no external mapping is used.

Possible business rule: corridor/party roles jointly select currency. Alternative:
mixtures of bank pairs within countries can produce the same result. This pass does
not control individual bank pair, so country-conditional differences are provisional.

## T2 · Time construction

Question: after normalizing weekdays for the number of observed calendar days, are UTC
hour/weekday patterns consistent by sender BIC-country code and customer-type pair,
and does July reproduce earlier patterns? Remove partial April30/July31 calendar days.

Possible rule: country- and customer-specific activity schedules. Alternatives: exposure
counts, bank-corridor composition, and UTC offsets. No external timezone table is used;
country-specific UTC modes cannot be interpreted directly as customer local hours.

## D2 · Duration construction

Question: are seconds explained by fixed additive increments for route type, observed
participants and FX count? Fit earlier-period least-squares seconds, compare route-only
baseline and evaluate July. Exact conditional duration quantiles/min/max/SD test whether
a deterministic formula can plausibly account for observed variation.

Possible mechanism: more processing steps add delay. Alternatives: route mixture,
unobserved bank processing modes, threshold/time-of-day processes. A low-explanatory-power
linear model is an informative negative result, not proof that participants/FX never matter.

## Outputs and scope

`investigate.py` saves exact full-census counts/quantiles, logged execution and compact
numeric cache in ignored outputs. Initial conclusions are saved before debate. These
tests do not prove causal direction, recover generator source, or estimate real economies.
