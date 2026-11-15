"""Exploratory labeled campaign size/ordering; provisional pending independent review."""
from pathlib import Path
import pandas as pd
import numpy as np
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
d=pd.read_csv(ROOT/'analysis/round2/c/relevant_pair_history.csv.gz',dtype=str,keep_default_na=False)
r=d[d.anomaly_type.eq('ROMANCE_SCAM')].copy();r['record']=r.source_record.astype('int64');r['time']=r.epoch_seconds.astype('int64')
g=r.groupby(['ordering_account','beneficiary_account']).agg(n=('record','size'),first_source=('record','min'),last_source=('record','max'),currencies=('currency_code','nunique'),timestamps=('time','nunique'))
counts=g.n.value_counts().sort_index();counts.to_csv(OUT/'romance_episode_size_counts.csv',header=['episodes'])
blank_in_pairs=d.merge(r[['ordering_account','beneficiary_account']].drop_duplicates(),on=['ordering_account','beneficiary_account']).anomaly_type.eq('').sum()
summary={'records':len(r),'exact_pairs':len(g),'blank_in_pairs':int(blank_in_pairs),'size_counts':counts.to_dict(),
 'single_currency_pairs':int(g.currencies.eq(1).sum()),'consecutive_source_pairs':int((g.last_source-g.first_source+1).eq(g.n).sum()),
 'repeated_timestamp_pairs':int(g.timestamps.lt(g.n).sum()),'uniform_2_to_8_pearson':float(((counts-500/7)**2/(500/7)).sum())}
print(summary)
pd.DataFrame([summary]).to_json(OUT/'romance_episode_initial.json',orient='records',indent=2)
