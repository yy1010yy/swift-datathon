# B independent currency-mode temporal initial

Before reading C currency-mode output. From own full raw10M scan saved joint counts,
learn each sender/receiver BICcountrycode's most frequent payment currency using every
pre-July record. No external currency map. Modes are learned without customer-type
conditioning; score all2,899,279Julyrecords by customer-type pair.

| Party pair | July records | Sender-country-mode correct | Receiver-country-mode correct |
|---|---:|---:|---:|
| BB |658937|588569|213139|
| BC |1623722|1452170|522494|
| CB |177180|158230|56473|
| CC |439440|393784|140458|

AllJulyrecords have known sender and receiver codes. Sender-country mode predicts
approximately89%of currencies across all fourroles, versus approximately32%forreceiver
mode. Candidate construction: paymentcurrency usually follows sendercountry's latent
defaultcurrency. This is a temporal predictive association, not a proven causal preference
or an exact90%Bernoulli source. Othercurrency sampling can coincide with senderdefault;
countrycode may proxy bank/corridor or generator choices. Fixed bankpair comparisons
and explicit alternativecurrency distribution remain needed. Results include all labels;
no inference of realcountry trade sizes or realcurrencyareas.

Scripts/logs/tables:currency_predictors.py,currency_predictors_run.log,
currency_temporal_modes.json,currency_temporal_predictions.csv; original full joint
counts currency_counts.csv. EarliestpartialApril30 is included in discovery, never July.
