# C independent initial currency-mode comparison

Saved before seeing the lead's withheld currency predictions. Input is reviewer B's
full-file 10M country-code-corridor×party×currency×period counts; C independently
implemented mode fitting and July scoring. This is shared extracted input, not a
separate raw extraction. No external currency/country map was consulted.

Question: Does payment currency tend to follow the sending side more than receiving
side? Candidate mechanism: customers choose an institution/country-associated currency
on the sending side. Alternative: receiving-side preferences or one global dominant
currency explains the observed choice.

Fit on all dates before July 1 UTC: for each sender BIC-country-like code, choose its
most frequent payment currency; independently choose each receiver code's most frequent
received currency. Ties resolve lexically. Predict July and compare a global early-mode
baseline (EUR). The receiver map measures received traffic mix; it is not a map of
official or native currencies.

July evaluation covers all 2,899,279 rows including labels, no missing/unseen codes:

| Heuristic | Correct July records |
|---|---:|
| Sender code's earlier modal currency | 2,592,753 |
| Receiver code's earlier modal received currency | 932,564 |
| Observed currency matches either modal currency | 2,727,417 |
| Global earlier modal currency EUR | 926,598 |

Sender-side preference explains about89.4% versus32.2% receiver-mode and32.0% global.
This supports a strong sending-side currency preference. The universal sender-mode
rule fails on306,526 July rows; even either-mode coverage leaves171,862 unexplained.
Party-pair strata all preserve the sender advantage (`currency_modes.json`).

Limits: the "either" result is coverage, not a single prediction available before
seeing the payment. Currency-mode maps are observed preferences, not official monetary
areas. Bank selection, corridor composition, global currencies and latent customer
purposes could drive the pattern. This initial comparison cannot identify exact mixture
probabilities or show that sender location causes currency choice. Need independent
lead reconciliation and exceptions by corridor/support before final wording.

Methods/results: `currency_modes.py`, `currency_modes.json`, learned mode CSVs,
`currency_mode_corridors.csv`, actual execution logs.
