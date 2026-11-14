"""Compare independently computed full-population tables; no new raw-data scan."""
from pathlib import Path
import json
import pandas as pd

root = Path(__file__).resolve().parents[1]
out = root/'outputs/eda_initial'
a = pd.read_csv(root/'analysis/reviews/a/route_counts.csv')
b = pd.read_csv(root/'analysis/reviews/b/joint_counts.csv')
lead = pd.read_csv(out/'route_counts.csv')
names = ['continuity','route','participants','entries','visible','distinct','gaps','invalid']
a = a.rename(columns={'flag':'continuity','other':'invalid'})
b = b.rename(columns={'distinct_visible':'distinct'})
lead = lead.rename(columns={'route_type':'route','participant_count':'participants',
    'visible_entries':'visible','distinct_visible_bics':'distinct','gap_entries':'gaps',
    'unknown_entries':'invalid'})
lead['entries'] = lead.visible+lead.gaps+lead.invalid
def grouped(d,keys,n):
    return d.groupby(keys)[n].sum().sort_index().rename('records')
pd.testing.assert_series_equal(grouped(a,names,'count'),grouped(b,names,'n'))
pd.testing.assert_series_equal(grouped(a,names,'count'),grouped(lead,names,'records'))
months = pd.read_csv(out/'route_month.csv').rename(columns={'route_type':'route','month_utc':'period'})
a['difference'] = a.participants-a.visible
pd.testing.assert_series_equal(grouped(a,['continuity','route','difference','period'],'count'),
    grouped(months,['continuity','route','difference','period'],'records'))
months['period'] = months.period.map(lambda m:'early' if m<'2023-07' else 'late')
b['difference'] = b.participants-b.visible
pd.testing.assert_series_equal(grouped(b,['continuity','route','difference','period'],'n'),
    grouped(months,['continuity','route','difference','period'],'records'))
flags=pd.read_csv(out/'route_diagnostics.csv').rename(columns={'route_type':'route'})
for flag,col in [('path_ordering_endpoint_mismatch','sender_mismatch'),
                 ('path_beneficiary_endpoint_mismatch','receiver_mismatch')]:
    sub=flags[flags.diagnostic.eq(flag)].rename(columns={'present':col})
    pd.testing.assert_series_equal(grouped(b,['continuity','route',col],'n'),
        grouped(sub,['continuity','route',col],'records'))
profile=json.loads((root/'outputs/cleaned/profile.json').read_text())
aa=json.loads((root/'analysis/reviews/a/summary.json').read_text())['labels']
ll=pd.read_csv(out/'labels.csv',keep_default_na=False)
bb=pd.read_csv(root/'analysis/reviews/b/labels.csv',keep_default_na=False)
bb['label']=bb.label.replace({'no recorded anomaly label':''})
assert aa==dict(zip(ll.anomaly_type,ll.records))==dict(zip(bb.label,bb.n))==profile['category_counts']['anomaly_type']
result={'status':'PASS','population':10000000,
    'checks':['A vs B vs lead exact joint route aggregates',
              'A vs lead exact monthly aggregates', 'B vs lead pre-July/July aggregates',
              'B vs lead endpoint diagnostics by flag and route',
              'A vs B vs lead vs original profile label census'],
    'participant_visible_equal':int(lead.loc[lead.participants.eq(lead.visible),'records'].sum()),
    'repeated_bic_rows':int(lead.loc[lead.visible.ne(lead.distinct),'records'].sum()),
    'gap_flag_disagreements':int(lead.loc[lead.continuity.eq('N').ne(lead.gaps.gt(0)),'records'].sum()),
    'limits':['Descriptive stability checks; discovery used full file, no untouched holdout.',
              'Cannot identify hidden banks, generator causal order, recall mechanism, or economic intent.']}
(out/'review_verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
