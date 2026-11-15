"""Independent latent decimal-error model; early fit, July score, no history needed."""
from pathlib import Path
import json,math
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'analysis/round2/a'
table=pd.read_csv(OUT/'amount_conditional.csv',keep_default_na=False)
train=table[(table.period=='early')&table.currency.ne('__ALL_CURRENCIES__')].copy()
currencies=sorted(train.currency.unique());lookup={v:i for i,v in enumerate(currencies)}
X=np.zeros((len(train),len(currencies)+2))
for i,r in enumerate(train.itertuples()):
 X[i,lookup[r.currency]]=1;X[i,-2]=r.party[0]=='B';X[i,-1]=r.party[1]=='B'
y=train.mean_log10.to_numpy()*np.log(10);w=train.n.to_numpy()
coef=np.linalg.lstsq(X*np.sqrt(w)[:,None],y*np.sqrt(w),rcond=None)[0]
meanmap={cu:coef[ix] for cu,ix in lookup.items()}
train['mu']=X@coef
train['second_residual']=(train.std_log10*np.log(10))**2+(y-train.mu)**2
varmap={cu:np.average(g.second_residual,weights=g.n) for cu,g in train.groupby('currency')}
x=np.load(ROOT/'outputs/round2/a/numeric.npy',mmap_mode='r')
# Full labelled population and deterministic every997th blank as negative-control sample.
labels=x['label'].copy();keep=(labels!='')|((np.arange(len(x))%997==0)&(labels==''))
d=pd.DataFrame({'source_record':np.flatnonzero(keep)+1,'label':labels[keep],
 'currency':x['currency'][keep],'party':x['party'][keep],
 'amount':x['amount'][keep],'early':x['epoch'][keep]<1688169600})
del x
d['mu']=d.currency.map(meanmap)+d.party.str[0].eq('B')*coef[-2]+d.party.str[1].eq('B')*coef[-1]
d['sd']=np.sqrt(d.currency.map(varmap));d['log_amount']=np.log(d.amount)
unknown=d.mu.isna()|d.sd.isna();excluded=d.loc[unknown].copy();d=d.loc[~unknown].copy()
fat=d[d.label.eq('FAT_FINGER_MISTAKE')];early=fat[fat.early];july=fat[~fat.early]
def density(g,shifts):
 z=(g.log_amount.to_numpy()[:,None]-g.mu.to_numpy()[:,None]-np.asarray(shifts)[None,:])/g.sd.to_numpy()[:,None]
 return np.maximum(np.exp(-.5*z*z)/(g.sd.to_numpy()[:,None]*np.sqrt(2*np.pi)),1e-300)
def fit(g,shifts):
 f=density(g,shifts);weights=np.ones(len(shifts))/len(shifts)
 for _ in range(10000):
  resp=f*weights;resp/=resp.sum(axis=1,keepdims=True);new=resp.mean(axis=0)
  if np.max(abs(new-weights))<1e-10:break
  weights=new
 return weights
models={'unchanged':([0.],np.array([1.]))}
weightrows=[]
for maxpower in [3,6]:
 powers=np.arange(-maxpower,maxpower+1);shifts=powers*np.log(10);weights=fit(early,shifts)
 models[f'decimal_mixture_pm{maxpower}']=(shifts,weights)
 for power,weight in zip(powers,weights):weightrows.append([maxpower,int(power),float(weight)])
# An unrestricted continuous shift provides a selection/scale competing explanation.
precision=1/early.sd.to_numpy()**2
continuous=float(np.average(early.log_amount-early.mu,weights=precision))
models['continuous_shift']=([continuous],np.array([1.]))
models['equal_weights_example_powers']=([-2*np.log(10),np.log(10),2*np.log(10),3*np.log(10),4*np.log(10)],np.ones(5)/5)
# Broader lognormal selection alternative, allowing both center and variance to change.
best=None
for tau in np.linspace(0,8,1601):
 variances=early.sd.to_numpy()**2+tau**2
 loc=np.average(early.log_amount-early.mu,weights=1/variances)
 loss=float(np.mean(.5*np.log(2*np.pi*variances)+.5*(early.log_amount-early.mu-loc)**2/variances))
 if best is None or loss<best[0]:best=(loss,float(loc),float(tau))
modelrows=[]
for label,g in d.assign(label=d.label.replace({'':'__BLANK_SAMPLE__'})).groupby('label'):
 for phase,gg in g.groupby('early'):
  for name,(shifts,weights) in models.items():
   score=float(-np.log(density(gg,shifts)@weights).mean())
   modelrows.append([label,'early' if phase else 'july',name,len(gg),score])
  variance=gg.sd.to_numpy()**2+best[2]**2
  score=float(np.mean(.5*np.log(2*np.pi*variance)+.5*(gg.log_amount-gg.mu-best[1])**2/variance))
  modelrows.append([label,'early' if phase else 'july','continuous_shift_extra_variance',len(gg),score])
scores=pd.DataFrame(modelrows,columns=['label','period','model','n','mean_nll_logamount'])
scores.to_csv(OUT/'fat_latent_scores.csv',index=False)
pd.DataFrame(weightrows,columns=['max_power','power10_shift','early_fitted_weight']).to_csv(OUT/'fat_latent_weights.csv',index=False)
d['residual']=d.log_amount-d.mu;d['standardized_residual']=d.residual/d.sd
d.to_csv(OUT/'fat_latent_row_evidence.csv',index=False)
summary=d.assign(label=d.label.replace({'':'__BLANK_SAMPLE__'})).groupby(['label','early']).agg(n=('amount','size'),mean_residual=('residual','mean'),median_residual=('residual','median'),sd_residual=('residual','std'))
summary.to_csv(OUT/'fat_latent_residual_summary.csv')
manifest={'baseline':'early blank-label weighted log-mean additive currency+senderBusiness+receiverBusiness; currency residual SD',
 'sender_business_shift_ln':float(coef[-2]),'receiver_business_shift_ln':float(coef[-1]),
 'blank_training_rows':int(train.n.sum()),'unknown_currency_exclusions':int(unknown.sum()),'fat_early':len(early),'fat_july':len(july),
 'continuous_shift_ln':continuous,'continuous_scale':math.exp(continuous),
 'continuous_extra_variance_fit':{'location':best[1],'extra_log_sd':best[2],'early_nll':best[0]},
 'limitations':['Normal logamount baseline approximate; heaping and bank mix remain.',
 'Latent amount shifts do not identify actual earlier intended transfer or unique error mechanism.',
 'Negative-control sample deterministic every997th blank record; no sampling representation claim.']}
(OUT/'fat_latent_manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(manifest,indent=2));print(pd.DataFrame(weightrows,columns=['max_power','power10_shift','weight']).to_string(index=False))
print(scores[scores.label.eq('FAT_FINGER_MISTAKE')].to_string(index=False));print(summary.to_string())
