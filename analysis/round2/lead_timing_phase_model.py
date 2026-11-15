"""Infer shared circular weekly timing template and sender-code phase shifts.

Uses only supplied UTC timestamps summarized by BIC country-like code. Phase labels
are relative to the data; no external timezone or country information is used.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
P=Path(__file__).resolve().parent
d=pd.read_csv(P/'b/timing_counts.csv',keep_default_na=False)
codes=sorted(d.sender_country_code.unique());index={c:i for i,c in enumerate(codes)}
early=np.zeros((len(codes),168),float);july=np.zeros_like(early)
for r in d.itertuples(index=False):
    target=early if r.period=='MayJune' else july
    target[index[r.sender_country_code],int(r.weekday)*24+int(r.hour)]+=r.n
exp_early=np.repeat([9,9,9,9,9,8,8],24).astype(float)
exp_july=np.repeat([4,4,4,4,4,5,5],24).astype(float)

def probabilities(rate, exposure):
    v=np.maximum(rate*exposure,1e-300);return v/v.sum()
def nll(counts,probs):return float(-(counts*np.log(np.maximum(probs,1e-300))).sum()/counts.sum())

global_rate=(early/exp_early).sum(axis=0)+1e-6
global_prob=probabilities(global_rate,exp_july)
global_nll=nll(july.sum(axis=0),global_prob)

# Direct country-specific weekly profile with shrinkage to global profile.
direct_scores=[]
for alpha in [10,100,1000]:
    ll=nn=0.
    base=global_rate/global_rate.sum()
    for i in range(len(codes)):
        rate=early[i]/exp_early
        fitted=rate+alpha*base
        p=probabilities(fitted,exp_july);ll+=(july[i]*np.log(p)).sum();nn+=july[i].sum()
    direct_scores.append({'alpha':alpha,'n':int(nn),'july_nll':float(-ll/nn)})

# Initialize against the largest sender code, then alternate phase and template.
ref_i=int(np.argmax(early.sum(axis=1)));template=early[ref_i]/exp_early+1e-6
offset=np.zeros(len(codes),int)
history=[]
for iteration in range(20):
    old=offset.copy()
    for i in range(len(codes)):
        if early[i].sum()==0:continue
        scores=[]
        for s in range(168):
            p=probabilities(np.roll(template,-s),exp_early) # UTC u uses local template u+s.
            scores.append((early[i]*np.log(p)).sum())
        offset[i]=int(np.argmax(scores))
    aligned=np.zeros(168,float)
    for i,s in enumerate(offset):
        aligned+=np.roll(early[i]/exp_early,s)
    template=aligned+1e-6
    changes=int((old!=offset).sum());history.append(changes)
    if changes==0:break

ll=nn=0.;phase_rows=[]
for i,code in enumerate(codes):
    s=int(offset[i]);rate=np.roll(template,-s);p=probabilities(rate,exp_july)
    ll+=(july[i]*np.log(p)).sum();nn+=july[i].sum()
    phase_rows.append(dict(sender_country_code=code,relative_phase_hours=s,
      early_n=int(early[i].sum()),july_n=int(july[i].sum()),july_nll=nll(july[i],p) if july[i].sum() else np.nan))
phase_nll=float(-ll/nn)
pd.DataFrame(phase_rows).to_csv(P/'timing_sender_phase.csv',index=False)
pd.DataFrame({'weekly_hour':range(168),'weekday':np.arange(168)//24,'hour':np.arange(168)%24,
 'relative_rate':template/template.mean()}).to_csv(P/'timing_shared_week_template.csv',index=False)

# Apply inferred phases to raw dates to test round weekly target volumes. This uses
# B's shared full numeric extraction and keeps the result an independent aggregation.
ROOT=P.parents[1];a=np.load(ROOT/'outputs/eda_round2/b_rows.npy',mmap_mode='r')
code_arr=np.char.decode(a['country'],'ascii');phase_map={r['sender_country_code']:r['relative_phase_hours'] for r in phase_rows}
ph=np.fromiter((phase_map.get(x,0) for x in code_arr),dtype='int16',count=len(a))
local_epoch=a['epoch']+ph.astype('int64')*3600
start=np.datetime64('2023-05-01','D').astype('int64');local_day=local_epoch//86400-start
keep=(local_day>=0)&(local_day<91)
local_week=(local_day[keep]//7).astype(int)
local_week_counts=np.bincount(local_week,minlength=13)
targets=np.rint(local_week_counts/50000)*50000
# Compare the transparent 50k grid and the exact set summing to 10m.
weekly=pd.DataFrame({'week':range(1,14),'phase_adjusted_records':local_week_counts,
 'nearest_50000':targets,'difference':local_week_counts-targets})
weekly.to_csv(P/'timing_phase_adjusted_weeks.csv',index=False)

result={'status':'complete','codes':len(codes),'reference_code':codes[ref_i],
 'iterations':len(history),'offset_changes':history,'july_rows':int(nn),
 'global_week_profile_nll':global_nll,'direct_country_profile_scores':direct_scores,
 'shared_template_phase_nll':phase_nll,
 'shared_template_vs_global_improvement':global_nll-phase_nll,
 'phase_adjusted_complete_window_rows':int(local_week_counts.sum()),
 'phase_adjusted_week_counts':local_week_counts.tolist(),
 'nearest_50000_targets':targets.astype(int).tolist(),
 'max_abs_week_target_difference':int(abs(local_week_counts-targets).max()),
 'limits':['Relative phase is data-derived and must not be called a real timezone.',
  'Template initialization/rotation is not unique; offsets are relative to the chosen reference.',
  'Direct country-specific profiles have many more parameters than a shared shifted template.',
  'Local-phase boundary shifting changes which records fall inside the fixed 13-week UTC window.',
  'Nearest-50k targets were proposed after inspecting UTC weekly totals and are exploratory.']}
(P/'timing_phase_model.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));print(weekly.to_string(index=False))
