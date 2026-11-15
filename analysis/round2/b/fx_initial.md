# B initial latent-zone result before lead/A zone results

Shared input: A's full-direct-route country-code/currency/FX joint census6,323,280
rows; country code comes from first/last visible path BICs. Construct an undirected
graph joining country codes whenever any Direct payment between them hasFX0.

There are167 connected components,11containing multiple codes. PredictFX1 if endpoints
are in different components, otherwiseFX0. It matches **6,323,280/6,323,280** Direct
records. Graph construction forces FX0 edges to match, but not FX1 edges; zero
within-component FX1 contradictions is additional evidence for a coherent zone partition.
This is all-data discovery, not temporal validation. Full components saved in
fx_components.csv and fx_initial.json. No external country/currency mapping was used.

Alternative inference: for each country code with any same-country Direct payments,
learn its modal payment currency from those payments. Different inferred currencies
predictFX1; same currenciesFX0. On the5,948,508payments with both endpoints covered
by this smaller inference, **all5,948,508match**. Many sparse codes lack same-country
observations, leaving374,772unscored; do not call them failures or silently impute.

A payment-currency-based alternative predicts one conversion for each endpoint whose
inferred local currency differs from the payment's currency. It matches5,865,111of
the same5,948,508known-code records and fails83,397. Thus endpoint currency-zone
boundaries explain Direct FX better than this simple payment-currency heuristic.

Possible mechanism: traversing banks in the same latent currency zone incurs no FX,
crossing a zone boundary incurs one. It remains necessary to train the partition only
on pre-July Directs and test July plus longer continuous routes. Gapped routes cannot
reveal actual hidden transitions. The number167is observational and could split zones
that lack links; these components do not establish complete real-world currency areas.

Execution:fx_zones.py,fx_run.log. Initial attempt asserted every code had same-country
training payments; that assertion failed. Corrected method marks these codes missing
and reports its denominator explicitly; no inferred currencies were fabricated.
