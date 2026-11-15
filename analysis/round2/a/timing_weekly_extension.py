"""Independent weekly timing templates and calendar factorization."""
from pathlib import Path
import pandas as pd,numpy as np,json
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'analysis/round2/a'
d=pd.read_csv(ROOT/'analysis/round2/b/timing_counts.csv',keep_default_na=False)
train=d[d.period.eq('MayJune')];test=d[d.period.eq('July')]
e0=np.repeat(np.array([9,9,9,9,9,8,8.]),24);e1=np.repeat(np.array([4,4,4,4,4,5,5.]),24)
codes=sorted(train.sender_country_code.unique());index={c:i for i,c in enumerate(codes)}
tr=np.zeros((len(codes),168));te=np.zeros_like(tr)
for g,arr in [(train,tr),(test,te)]:
 for r in g.itertuples():arr[index[r.sender_country_code],r.weekday*24+r.hour]+=r.n
scores=[];templates=[]
for alpha in [.1,.5,1,5,20,100]:
 for smooth in [False,True]:
  rate=(tr+alpha)/e0
  if smooth:rate=(np.roll(rate,1,axis=1)+2*rate+np.roll(rate,-1,axis=1))/4
  pred=rate*e1;pred/=pred.sum(axis=1,keepdims=True)
  score=float(-(te*np.log(pred)).sum()/te.sum())
  totals=te.sum(axis=1);positive=totals>0
  tv=float(np.sum(.5*np.abs(te[positive]/totals[positive,None]-pred[positive]).sum(axis=1)*totals[positive])/te.sum())
  scores.append([alpha,smooth,score,tv,int(te.sum())])
  if alpha==.5 and not smooth:
   for i,country in enumerate(codes):
    for j in range(168):templates.append([country,j,j//24,j%24,int(tr[i,j]),float(rate[i,j]),float(pred[i,j])])
pd.DataFrame(scores,columns=['alpha_per_cell','cyclic_121_smoothing','July_nll','weighted_TV','July_n']).to_csv(OUT/'timing_weekly_template_scores.csv',index=False)
pd.DataFrame(templates,columns=['sender_country_code','hour_of_week','weekday','hour_utc','early_count','early_rate','July_pred_probability']).to_csv(OUT/'timing_weekly_templates.csv',index=False)
# Shared weekly activity template with data-inferred integer shifts; no external timezones.
weights=tr.sum(axis=1);rates=(tr+.5)/e0;normalized=rates/rates.sum(axis=1,keepdims=True)
template=normalized[np.argmax(weights)].copy();shifts=np.zeros(len(codes),dtype=int)
options=np.arange(-24,25)
for iteration in range(30):
 for i in range(len(codes)):
  candidates=np.stack([np.roll(template,int(s)) for s in options])*e0
  candidates/=candidates.sum(axis=1,keepdims=True)
  shifts[i]=options[np.argmax((tr[i]*np.log(candidates)).sum(axis=1))]
 new=sum(weights[i]*np.roll(normalized[i],-int(shifts[i])) for i in range(len(codes)))/weights.sum()
 if np.max(abs(new-template))<1e-10:break
 template=new
pred=np.stack([np.roll(template,int(s)) for s in shifts])*e1;pred/=pred.sum(axis=1,keepdims=True)
phase_nll=float(-(te*np.log(pred)).sum()/te.sum())
pd.DataFrame({'sender_country_code':codes,'relative_fitted_hour_shift':shifts,'early_n':weights.astype(int)}).to_csv(OUT/'timing_shared_phase_shifts.csv',index=False)
pd.DataFrame({'hour_of_week':np.arange(168),'learned_template_rate':template}).to_csv(OUT/'timing_shared_phase_template.csv',index=False)
# Exact 13 complete weeks cannot be recovered from period-collapsed table; use shared B raw cache.
x=np.load(ROOT/'outputs/eda_round2/b_rows.npy',mmap_mode='r');epoch=x['epoch'].copy();countries=x['country'].copy();party=x['party'].copy();del x
start=int(pd.Timestamp('2023-05-01',tz='UTC').timestamp());stop=int(pd.Timestamp('2023-07-31',tz='UTC').timestamp())
keep=(epoch>=start)&(epoch<stop);day=((epoch[keep]-start)//86400).astype(int);week=day//7;weekday=day%7
g=pd.DataFrame({'week':week,'weekday':weekday,'sender_country_code':pd.Categorical(countries[keep].astype(str)),'party':party[keep]})
weektable=g.value_counts(sort=False).rename('n').reset_index();weektable.to_csv(OUT/'timing_complete_week_counts.csv',index=False)
mat=np.zeros((13,7),dtype='int64')
for r in weektable.itertuples():mat[r.week,r.weekday]+=r.n
tot=mat.sum();expected=np.outer(mat.sum(axis=1),mat.sum(axis=0))/tot
ratios=mat/expected;weekshares=mat.sum(axis=1)/tot
weekout=[]
for w in range(13):
 for wd in range(7):weekout.append([w+1,wd,int(mat[w,wd]),float(expected[w,wd]),float(ratios[w,wd])])
pd.DataFrame(weekout,columns=['week','weekday','observed','expected_weekXweekday','observed_over_expected']).to_csv(OUT/'timing_week_day_factorization.csv',index=False)
pd.DataFrame({'week':np.arange(1,14),'n':mat.sum(axis=1),'share':weekshares,'nearest_005':np.round(weekshares/.005)*.005,'quantization_error':weekshares-np.round(weekshares/.005)*.005}).to_csv(OUT/'timing_week_volume_quantization.csv',index=False)
print(pd.DataFrame(scores,columns=['alpha','cyclic','July_nll','TV','n']).to_string(index=False))
print('Shared shifted-template JulyNLL',phase_nll,'iterations',iteration+1)
print('Completeweekrows',int(tot),'global factorization TV',float(.5*np.abs(mat-expected).sum()/tot),'ratio minmax',ratios.min(),ratios.max())
print('Weekshares',weekshares,'nearest .005 error',weekshares-np.round(weekshares/.005)*.005)
print('Quantization of only13 exploratory shares is not sufficient evidence of an exact choice grid; countrycode/dateboundary stratification required.')
(OUT/'timing_week_extension_manifest.json').write_text(json.dumps({'conditional_July_n':int(te.sum()),'complete_13week_n':int(tot),'shared_shift_template_July_nll':phase_nll,'shift_iterations':iteration+1,'week_factorization_TV':float(.5*np.abs(mat-expected).sum()/tot),'shared_inputs':['B timing_counts.csv','B raw numeric cache b_rows.npy']},indent=2))
