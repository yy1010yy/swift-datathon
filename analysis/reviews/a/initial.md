# Reviewer A initial conclusion

Status: independent initial result, before seeing reviewer B's findings.

All 10,000,000 records were processed by `analysis/review_a.py`. No rows were
excluded. `participant_count` equals the number of visible valid BIC **entries**
in 10,000,000 / 10,000,000 rows, separately in all six continuity/route strata.
This is a candidate reconstructed field rule, not proof of the hidden program.

All 767,204 continuity-N paths contain literal gaps; none of the 9,232,796
continuity-Y paths contain gaps. Counting all semicolon-delimited tokens produces
a mismatch in exactly the 767,204 N rows. There are no other malformed tokens.

Counting distinct BICs changes the result: 59,191 records repeat a visible BIC,
including six Y/Direct records. Reported participants therefore should not be
described as the number of distinct institutions. The distinct-count mismatch
breakdown is N/Covered 1,827; N/Indirect 8,176; Y/Covered 9,566;
Y/Direct 6; Y/Indirect 39,616; N/Direct 0.

The independent label census reproduces all profile counts: no recorded anomaly
label 9,992,994; ROMANCE_SCAM 2,476; FAT_FINGER_MISTAKE 1,940;
ACCOUNT_REPLACEMENT_SCAM 649; CEO_SCAM 945; DUPLICATE_PAYMENT 679;
CUSTOMER_RECALL 317. The last label's generating mechanism remains untested.

Strongest unresolved uncertainty: the data do not reveal how many real or
synthetic intermediaries a `...` gap represents. Equality to visible entries
does not establish complete routing visibility, economic causes, or duration/FX
effects. Competing explanation to test: participant count may refer to distinct
institutions; the repeated-BIC records discriminate between these definitions.

Evidence: `route_counts.csv`, `summary.json`, `examples.csv`, and `method.md`
in this directory. The example file contains first-encountered cases only.
