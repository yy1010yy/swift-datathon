"""Endpoint perturbation independence model from independently parser-verified B census."""
from pathlib import Path
import json
import pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
d=pd.read_csv(ROOT/'analysis/reviews/b/joint_counts.csv')
train=d[d.period.eq('early')]
ps=train.loc[train.sender_mismatch,'n'].sum()/train.n.sum();pr=train.loc[train.receiver_mismatch,'n'].sum()/train.n.sum()
rows=[]
for (period,route,q),g in d.groupby(['period','route','continuity']):
 n=g.n.sum();s=g.loc[g.sender_mismatch,'n'].sum();r=g.loc[g.receiver_mismatch,'n'].sum();both=g.loc[g.sender_mismatch&g.receiver_mismatch,'n'].sum()
 cells=g.groupby(['sender_mismatch','receiver_mismatch']).n.sum().to_dict()
 expected={(sm,rm):n*(ps if sm else 1-ps)*(pr if rm else 1-pr) for sm in [False,True] for rm in [False,True]}
 rows.append(dict(period=period,route=route,continuity=q,n=int(n),sender=int(s),receiver=int(r),both=int(both),
   sender_rate=float(s/n),receiver_rate=float(r/n),both_rate=float(both/n),
   both_independence_expected=float(s*r/n),frozen_early_expected_both=float(n*ps*pr),
   frozen_early_joint_tv=float(sum(abs(cells.get(k,0)-e) for k,e in expected.items())/n/2)))
z=pd.DataFrame(rows);z.to_csv(OUT/'endpoint_model_strata.csv',index=False)
summary={'train_sender_rate':ps,'train_receiver_rate':pr,'rows':int(d.n.sum()),
 'sender_rate_range':list(map(float,[z.sender_rate.min(),z.sender_rate.max()])),
 'receiver_rate_range':list(map(float,[z.receiver_rate.min(),z.receiver_rate.max()])),
 'july_joint_tv':float((z.loc[z.period.eq('late'),'n']*z.loc[z.period.eq('late'),'frozen_early_joint_tv']).sum()/z.loc[z.period.eq('late'),'n'].sum()),
 'limits':'earlyincludespartialApril; sourceBtable hasperiodnotmonth. Endpoint mismatch doesnotidentify whichfield changed or whetherdata arecorrupt.'}
(OUT/'endpoint_model.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2));print(z.to_string(index=False))
