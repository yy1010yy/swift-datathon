# A independent account/detail construction initial

The full 10M-row scan in `account_construction.py` completed before comparison with
B's account result. It tested both sides, preserving exact account strings and actual
line breaks. All **20,000,000** account fields begin `_FAKE_`.

Let the identifier be the exact substring after `_FAKE_`. Removing all leading `/`
characters from the first detail line reproduces the identifier on **9,308,991**
ordering sides and **9,274,369** beneficiary sides. The exact identifier occurs
anywhere in the detail field on **9,436,890** ordering sides and **9,390,618**
beneficiary sides. Therefore account-to-detail copying is common but not universal:
563,110 ordering and 609,382 beneficiary fields contain no exact identifier.
Normalizing punctuation/case adds no matches in this implementation.

The suffix matches the script's IBAN-like format on 5,442,631 ordering and 5,405,035
beneficiary sides. Within this data-derived format class its first two letters always
match characters 5–6 of the corresponding BIC. This is a deterministic encoding
observation from the supplied data, not external IBAN validation.

## Full exact account/BIC reuse census

The disk-backed census retains every `(side, exact account, BIC)` occurrence:

| Side | Exact accounts | Account/BIC pairs | Repeated accounts | Accounts with multiple BICs | Maximum occurrences |
|---|---:|---:|---:|---:|---:|
| ordering | 391,132 | 391,132 | 260,873 | 0 | 75,803 |
| beneficiary | 2,590,877 | 2,663,723 | 567,583 | 61,606 | 53,350 |

Across roles, 61,690 exact account strings occur with more than one BIC. Thus an exact
ordering account maps to one ordering BIC in this file, but a universal raw-account-to-
one-bank identity rule is false on the beneficiary side and across roles. The data do
not identify whether reused strings denote one real customer, multiple synthetic
entities, or role-specific assignments.

Evidence: `account_construction.py`, actual `account_initial.log`,
`account_detail_joint.csv`, `account_reuse_summary.json`, and class examples in
`account_detail_examples.csv`. The SQLite working database remains under ignored
`outputs/round2/a/`; the compact totals above are committed artifacts.

