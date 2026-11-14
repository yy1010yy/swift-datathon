"""Independent full-population routing estimate, reviewer A. No row filtering."""
from collections import Counter
from pathlib import Path
import json
import re
import time
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'analysis/reviews/a'
OUT.mkdir(parents=True, exist_ok=True)
columns = ['bic8_path','participant_count','continuity_qflag','transaction_type_code','anomaly_type','epoch_seconds']
counts = Counter()
labels = Counter()
examples = []
rows = 0
started = time.monotonic()
valid = re.compile(r'[A-Z0-9]{8}').fullmatch
for chunk in pd.read_csv(ROOT/'outputs/cleaned/payments_cleaned.csv.gz', usecols=columns, dtype='str', keep_default_na=False, chunksize=100000):
    parsed = {}
    for path in chunk.bic8_path.unique():
        entries = path.split(';')
        visible = [s for s in entries if valid(s)]
        parsed[path] = (len(entries), len(visible), len(set(visible)), entries.count('...'), sum(not valid(s) and s != '...' for s in entries))
    work = pd.DataFrame(chunk.bic8_path.map(parsed).tolist(), columns=['entries','visible','distinct','gaps','other'], index=chunk.index)
    work['participants'] = chunk.participant_count.astype(int)
    work['flag'] = chunk.continuity_qflag
    work['route'] = chunk.transaction_type_code
    work['period'] = pd.to_datetime(chunk.epoch_seconds.astype('int64'), unit='s', utc=True).dt.strftime('%Y-%m')
    keys = ['flag','route','period','participants','entries','visible','distinct','gaps','other']
    counts.update(work.value_counts(subset=keys).to_dict())
    labels.update(chunk.anomaly_type)
    if len(examples) < 12:
        mask = work.visible.ne(work.participants) | work.distinct.ne(work.visible)
        for idx in work.index[mask][:12-len(examples)]:
            examples.append({**chunk.loc[idx].to_dict(), **work.loc[idx].to_dict()})
    rows += len(chunk)
    if rows % 1000000 == 0:
        print(f'A: {rows:,} rows, {time.monotonic()-started:.1f}s', flush=True)
table = pd.DataFrame([dict(zip(keys,k), count=n) for k,n in counts.items()])
table.to_csv(OUT/'route_counts.csv', index=False)
pd.DataFrame(examples).to_csv(OUT/'examples.csv', index=False)
result = {'rows':rows, 'labels':dict(labels), 'elapsed_seconds':time.monotonic()-started}
for (flag,route), g in table.groupby(['flag','route']):
    result[f'{flag}/{route}'] = {'rows':int(g['count'].sum()), 'visible_equals_participants':int(g.loc[g.visible.eq(g.participants),'count'].sum()), 'entries_equals_participants':int(g.loc[g.entries.eq(g.participants),'count'].sum()), 'distinct_equals_visible':int(g.loc[g.distinct.eq(g.visible),'count'].sum()), 'with_gap':int(g.loc[g.gaps.gt(0),'count'].sum()), 'other_path_tokens':int(g.loc[g.other.gt(0),'count'].sum()), 'visible_exceeds_participants':int(g.loc[g.visible.gt(g.participants),'count'].sum())}
(OUT/'summary.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps(result,indent=2))
