"""Circular week-hour shared-template model and 13-complete-week volume factorization."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
d=pd.read_csv(OUT/'timing_counts.csv',keep_default_na=False)
train=d[d.period.eq('MayJune')];test=d[d.period.eq('July')]
codes=sorted(set(d.sender_country_code));ci={v:i for i,v in enumerate(codes)}
x=np.zeros((len(codes),168));y=x.copy()
for source,arr in [(train,x),(test,y)]:
 for r in source.itertuples():arr[ci[r.sender_country_code],r.weekday*24+r.hour]+=r.n
et=np.repeat([9.,9,9,9,9,8,8],24);ej=np.repeat([4.,4,4,4,4,5,5],24)
f=(x.sum(axis=0)/et)+1e-6;f/=f.sum();shifts=np.zeros(len(codes),dtype=int)
trace=[]
for iteration in range(30):
 # P(UTCweekhour|code) ∝ calendar exposure×one shared circular profile shifted bycode.
 templates=np.array([np.roll(f,s)*et for s in range(168)])
 templates/=templates.sum(axis=1)[:,None]
 logscore=x@np.log(templates).T
 newshifts=np.argmax(logscore,axis=1)
 pooled=np.zeros(168);den=np.zeros(168)
 for i,s in enumerate(newshifts):
  rate=x[i].sum()/np.sum(et*np.roll(f,s))
  pooled+=np.roll(x[i],-s)
  den+=rate*np.roll(et,-s)
 newf=(pooled+1e-6)/(den+1e-6);newf/=newf.sum()
 loss=float(-np.take_along_axis(logscore,newshifts[:,None],axis=1).sum()/x.sum())
 trace.append(dict(iteration=iteration,train_nll=loss,changed_code_phases=int(np.sum(shifts!=newshifts))))
 f=newf;shifts=newshifts
scores=[]
for i,code in enumerate(codes):
 p=np.roll(f,shifts[i])*ej;p/=p.sum()
 for party,g in test[test.sender_country_code.eq(code)].groupby('party'):
  counts=np.zeros(168)
  for r in g.itertuples():counts[r.weekday*24+r.hour]+=r.n
  n=counts.sum();scores.append(dict(sender_country_code=code,party=party,n=int(n),phase=int(shifts[i]),
   nll=float(-np.sum(counts*np.log(p))/n),tv=float(np.sum(np.abs(counts/n-p))/2)))
s=pd.DataFrame(scores);s.to_csv(OUT/'timing_circular_strata.csv',index=False)
pd.DataFrame(trace).to_csv(OUT/'timing_circular_trace.csv',index=False)
pd.DataFrame({'template_weekhour':np.arange(168),'probability':f}).to_csv(OUT/'timing_circular_template.csv',index=False)
res={'model':'one shared168hourtemplate + integercodephase, alternating fitted30iterations',
 'july_rows':int(s.n.sum()),'july_nll':float(np.average(s.nll,weights=s.n)),
 'july_conditional_tv':float(np.average(s.tv,weights=s.n)),
 'limits':'phases can shift any0..167hours and are not identified localtimezones; alternating localoptimum, no generatorproof'}
# Numeric fullcensus cache has timestamps; period-aggregate table alone lacksweekindex.
a=np.load(ROOT/'outputs/eda_round2/b_rows.npy',mmap_mode='r')
start=1682899200;stop=1690761600 # May1inclusive toJuly31exclusive, exactly13weeks.
day=(a['epoch']-start)//86400;mask=(a['epoch']>=start)&(a['epoch']<stop)
cnt=np.bincount(day[mask].astype('i4'),minlength=91).reshape(13,7)
assert cnt.sum()==int(s.n.sum()+train.n.sum())
expected=cnt.sum(axis=1)[:,None]*cnt.sum(axis=0)[None,:]/cnt.sum()
relative=(cnt-expected)/expected
res.update({'complete_weeks':13,'week_day_rows':int(cnt.sum()),
 'week_day_factorization_tv':float(np.abs(cnt-expected).sum()/cnt.sum()/2),
 'week_day_relative_rms':float(np.sqrt(np.mean(relative**2))),
 'week_day_max_abs_relative':float(np.abs(relative).max())})
pd.DataFrame([dict(week=i,weekday=j,observed=int(cnt[i,j]),rank1_expected=float(expected[i,j]),relative_residual=float(relative[i,j])) for i in range(13) for j in range(7)]).to_csv(OUT/'timing_weekday_factorization.csv',index=False)
(OUT/'timing_extension.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
print('Weektotals',cnt.sum(axis=1).tolist())
