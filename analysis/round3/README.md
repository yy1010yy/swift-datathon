# Round 3: four targeted generator gaps

Scope is limited to the four areas requested after the broad EDA:

1. exact bank/corridor effects;
2. entity, counterparty and correspondent-network formation;
3. CEO scam, account-replacement and customer-recall mechanisms;
4. processing-duration and alternative-currency rules.

Each area requires two independent sub-agent initials, exchanged challenges, a lead
deciding calculation and final wording. Scripts, actual logs and compact tables live
under `a/`, `b/`, `c/` and `lead/`. Large caches belong under ignored
`outputs/round3/`. The source is the unchanged 10M-row cleaned file. Earlier/July
comparisons are retrospective stability tests, not untouched holdouts.

Do not treat a better predictor as proof of causal direction. Exact BIC codes are
synthetic identifiers; country-code and bank/corridor interpretations are internal
data features rather than claims about real institutions or markets.

## Executed evidence index

| Area | Independent initials and code | Debate / lead decision |
|---|---|---|
| Bank/corridor, duration and currency | `b/initial.md`, `b/scan.py`, `b/models.py`; `c/initial.md`, `c/build_bank_cache.py`, `c/duration_currency_models.py` | `b/bank_duration_currency_debate.md`, `c/bank_duration_currency_debate.md`, `lead/core_verification.json`, `lead/duration_order_verification.json` |
| Entity and pair formation | `a/entity_network_initial.md`, `a/entity_network.py`; `b/initial.md`, `b/pair_activity.py` | `b/entity_network_debate.md`, `lead/core_verification.json` |
| Remaining anomalies | `c/initial.md`, `c/anomaly_initial.py`; `d/anomaly_initial.md`, `d/anomaly_review.py` | `d/anomaly_debate.md`, `lead/remaining_verification.json` |
| Visible intermediaries and exact-pair route choice | `b/initial.md`, `b/models.py`; `d/intermediary_initial.md`, `d/intermediary_review.py` | `d/intermediary_debate.md`, `lead/remaining_verification.json` |

The canonical stakeholder explanation remains `../round2/findings.md`; round 3 does
not create a second competing findings report. Preserved failed logs document the
cancelled redundant A bank scan, D corrections, C `NA` parsing correction and the
lead alpha/tolerance correction.

