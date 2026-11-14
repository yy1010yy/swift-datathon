# Independent initial conclusion B

Population: all 10,000,000 cleaned payments; no exclusions.

Question: Do reported participants count visible BIC occurrences, distinct institutions, or hidden path entries?

- all rows: 10,000,000
- visible occurrences equal participants: 10,000,000
- distinct visible BICs equal participants: 9,940,809
- visible BIC repetitions: 59,191
- literal gap present: 767,204
- unrecognized path entry: 0
- visible count greater than participants: 0
- gap present with continuity Y: 0
- no gap with continuity N: 0
- sender endpoint mismatch with no gap: 460,440
- receiver endpoint mismatch with no gap: 461,111

Initial candidate rule: participant_count equals the number of visible BIC occurrences, excluding literal gap markers. This is an exact observed relationship across the supplied population, including gapped routes. A distinct-institution count is contradicted by 59,191 rows with repeated visible BICs. This supports a visible-occurrence field construction; it does not establish the true number of hidden institutions.

Initial candidate rule: continuity N coincides with at least one literal gap and Y with none, with zero observed exceptions. Endpoint disagreement is a separate issue: 460,440 sender and 461,111 receiver endpoint mismatches remain on ungapped routes, so gap observability cannot explain them all.

Label reconciliation: the six nonblank counts match the original profile (7,006 total). CUSTOMER_RECALL has 317 records. Its mechanism remains unresolved; blank labels mean only no recorded anomaly label.

## Continuity, route and temporal self-consistency

Temporal split is July 1 2023 00:00 UTC; early/late are validation subgroups, not randomized.

```
continuity    route period    rows  visible_equal  distinct_equal  gapped
         N  Covered  early   36330          36330           35034   36330
         N  Covered   late   14932          14932           14401   14932
         N   Direct  early  223597         223597          223597  223597
         N   Direct   late   91669          91669           91669   91669
         N Indirect  early  284379         284379          278679  284379
         N Indirect   late  116297         116297          113821  116297
         Y  Covered  early  259440         259440          252643       0
         Y  Covered   late  105260         105260          102491       0
         Y   Direct  early 4266103        4266103         4266097       0
         Y   Direct   late 1741911        1741911         1741911       0
         Y Indirect  early 2030872        2030872         2002651       0
         Y Indirect   late  829210         829210          817815       0
```

Uncertainty: exact finite-population counts are not sampling estimates. Observational agreement cannot prove the generator code or the economic meaning of participant_count. Gapped routes do not expose all institutions; endpoint disagreement alone cannot establish corrupt routing. Repeated visible institutions, when present, distinguish occurrence counting from distinct-institution counting.

Calculation references: analysis/review_b.py and analysis/review_b_summary.py; outputs are joint_counts.csv, summary.csv, labels.csv and period_check.csv in this folder.