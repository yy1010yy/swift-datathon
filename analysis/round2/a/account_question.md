# Independent account/detail construction question

Before reading lead results, test all10M rows on each side: `_FAKE_` prefix coverage;
whether suffix equals first detail line after stripping leading slashes, is a literal
substring anywhere in details, or occurs after removing punctuation/whitespace.
Separate exact firstline/presence from weaker normalized matches and keep examples.
Count by month andpartytype. Missing details/accounts remain explicit exceptions.

IBAN-looking means only a syntactic twoletter+twodigit+alphanumeric suffix pattern,
not validation against an external country/IBAN registry. Compare its twoletter prefix
to corresponding bank BIC positions4:6. Test reuse of exact accounts and account/BIC
pairs, recording per-side and combined account assignments. An account consistently
copied into details supports field derivation, not independent corroboration or uniqueness.
Repeated accounts need not be accidental duplicate payments.

Full chunked raw cleaned scan, preserving text formatting and account strings. SQLite
aggregates exact account/BIC reuse on disk to avoid memory assumptions. Save actual
outputs, exact contingency tables and source-record examples; no external data.
