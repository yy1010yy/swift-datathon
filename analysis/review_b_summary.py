"""Summarize independently computed routing counts; run after review_b.py."""
from pathlib import Path
import pandas as pd

out = Path('analysis/reviews/b')
t = pd.read_csv(out/'joint_counts.csv')
lines = ['# Independent initial conclusion B', '',
         'Population: all 10,000,000 cleaned payments; no exclusions.', '',
         'Question: Do reported participants count visible BIC occurrences, distinct institutions, or hidden path entries?', '']
def count(mask): return int(t.loc[mask,'n'].sum())
for name, mask in {
    'all rows': t.n >= 0,
    'visible occurrences equal participants': t.visible == t.participants,
    'distinct visible BICs equal participants': t.distinct_visible == t.participants,
    'visible BIC repetitions': t.visible > t.distinct_visible,
    'literal gap present': t.gaps > 0,
    'unrecognized path entry': t.invalid > 0,
    'visible count greater than participants': t.visible > t.participants,
    'gap present with continuity Y': (t.gaps > 0) & (t.continuity=='Y'),
    'no gap with continuity N': (t.gaps == 0) & (t.continuity=='N'),
    'sender endpoint mismatch with no gap': t.sender_mismatch & (t.gaps == 0),
    'receiver endpoint mismatch with no gap': t.receiver_mismatch & (t.gaps == 0),
}.items():
    lines.append(f'- {name}: {count(mask):,}')
lines += ['', 'Initial candidate rule: participant_count equals the number of visible BIC occurrences, excluding literal gap markers. This is an exact observed relationship across the supplied population, including gapped routes. A distinct-institution count is contradicted by 59,191 rows with repeated visible BICs. This supports a visible-occurrence field construction; it does not establish the true number of hidden institutions.', '',
          'Initial candidate rule: continuity N coincides with at least one literal gap and Y with none, with zero observed exceptions. Endpoint disagreement is a separate issue: 460,440 sender and 461,111 receiver endpoint mismatches remain on ungapped routes, so gap observability cannot explain them all.', '',
          'Label reconciliation: the six nonblank counts match the original profile (7,006 total). CUSTOMER_RECALL has 317 records. Its mechanism remains unresolved; blank labels mean only no recorded anomaly label.', '',
          '## Continuity, route and temporal self-consistency', '',
          'Temporal split is July 1 2023 00:00 UTC; early/late are validation subgroups, not randomized.', '']
period=[]
for key,s in t.groupby(['continuity','route','period']):
    period.append(dict(zip(['continuity','route','period'], key), rows=int(s.n.sum()),
      visible_equal=int(s.loc[s.visible==s.participants,'n'].sum()),
      distinct_equal=int(s.loc[s.distinct_visible==s.participants,'n'].sum()),
      gapped=int(s.loc[s.gaps>0,'n'].sum())))
v=pd.DataFrame(period)
v.to_csv(out/'period_check.csv',index=False)
lines += ['```', v.to_string(index=False), '```', '',
          'Uncertainty: exact finite-population counts are not sampling estimates. Observational agreement cannot prove the generator code or the economic meaning of participant_count. Gapped routes do not expose all institutions; endpoint disagreement alone cannot establish corrupt routing. Repeated visible institutions, when present, distinguish occurrence counting from distinct-institution counting.', '',
          'Calculation references: analysis/review_b.py and analysis/review_b_summary.py; outputs are joint_counts.csv, summary.csv, labels.csv and period_check.csv in this folder.']
(out/'initial.md').write_text('\n'.join(lines),encoding='utf-8')
print('\n'.join(lines))
