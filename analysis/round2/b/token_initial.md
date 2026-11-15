# B independent token-country initial result

Before seeing lead or reviewer A token-country counts. Independent full raw-file scan,
10,000,000 rows, regex `<country_code:([^>]+)>`, separately each side. No external
country table. Bank-code reference is BIC characters4:6 (zero-indexed).

Ordering tokens:3,915,405 rows lack a country-code token. Every remaining6,084,595
has exactly one token and it agrees with the ordering bank's country code in all
6,084,595/6,084,595 cases. No multiple-country-token rows. This supports a strict
observed sender-side text/bank-country construction rule conditional on token presence.

Beneficiary tokens:3,892,642 rows lack the token; all other6,107,358 have exactly one.
Only59,826 agree with the beneficiary bank and88,333 with the ordering bank. The
country-code token agrees across parties on53,049 rows (joint presence denominator
available in token_country_joint.csv). Thus the sender-side deterministic rule does
not generalize to the receiver. A common-country/independent sampling process might
explain beneficiary mismatches, but this census alone does not identify how receiver
addresses or banks are chosen. Missing tokens do not imply missing bank geography.

All monthly/type joint cells are saved in token_country_joint.csv; run196.9seconds,
token_run.log and token_manifest.json. No original text/identifiers were modified.
