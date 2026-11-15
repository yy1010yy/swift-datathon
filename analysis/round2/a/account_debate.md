# A/B account/detail self-consistency and challenge

A and B completed separate raw 10M-row scans. They agree exactly that all 20M account
fields begin `_FAKE_`, and that the exact post-prefix identifier occurs somewhere in
details on **9,436,890 ordering** and **9,390,618 beneficiary** sides. A's
all-leading-slash first-line counts (**9,308,991 / 9,274,369**) exactly match B's
`strip_all_slash_match` counts. B's more careful one-or-more prefix test is the right
measure of first-line embedding because an identifier can itself start with `/`; it
gives the same totals as identifier-anywhere. No later-line-only occurrences were
observed. B also independently finds no literal backslash-`n` separators.

The strongest challenge is that `_FAKE_` plus frequent embedding does not make an
account a globally unique, immutable customer key. B's deterministic 3/256 account
sample finds 8,500 exact accounts with changing detail text and 731 with changing BIC.
A's full exact census strengthens the BIC boundary: ordering-side accounts have no
within-side BIC changes, while **61,606 beneficiary accounts** do; **61,690** exact
strings have multiple BICs across both roles. Both scans find no type inconsistency in
B's selected sample, but A did not census account/type reuse, so a global type-function
claim is not promoted.

## Final wording

**Every account field is a synthetic `_FAKE_` string. In roughly 94% of side records,
the exact suffix is copied into the first detail line after one or more slashes. The
remaining records use other detail formats. Account reuse is role-asymmetric: ordering
accounts map to one ordering BIC in the observed file, while tens of thousands of
beneficiary account strings occur with multiple BICs. Treat the exact string as an
observed identifier, not proof of a globally unique customer.**

This is an encoding/construction rule, not a causal economic rule. No missing embedding
or BIC change is automatically an error or anomaly. Deciding artifacts are A's full
reuse census and B's independent full embedding counts plus selected detail/BIC
consistency sample (`b/account_initial.md`).
