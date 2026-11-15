"""Independent numpy-binomial target encoding on shared B raw numeric cache."""
from pathlib import Path
import numpy as np,pandas as pd,json
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'analysis/round2/a'
a=np.load(ROOT/'outputs/eda_round2/b_rows.npy',mmap_mode='r')
mask=a['route']!=0;sender=a['country'][mask].copy();y=(a['route'][mask]==2).astype(float);early=a['epoch'][mask]<1688169600
countries,codes=np.unique(sender,return_inverse=True);K=len(countries)
n0=np.bincount(codes[early],minlength=K);k0=np.bincount(codes[early],weights=y[early],minlength=K)
n1=np.bincount(codes[~early],minlength=K);k1=np.bincount(codes[~early],weights=y[~early],minlength=K)
base=float(y[early].mean());alpha=100.
rates=(k0+alpha*base)/(n0+alpha)
pred=rates[codes[~early]];constant=np.full(len(pred),base);target=y[~early]
def nll(p):
 p=np.clip(p,1e-15,1-1e-15)
 return float(-(target*np.log(p)+(1-target)*np.log(1-p)).mean())
t=pd.DataFrame({'sender_country_code':np.char.decode(countries,'ascii'),'early_n':n0,'early_covered':k0.astype(int),'July_n':n1,'July_covered':k1.astype(int),'fixed_alpha100_pred':rates})
t['early_raw_rate']=np.divide(k0,n0,out=np.full(K,np.nan),where=n0>0)
t['July_raw_rate']=np.divide(k1,n1,out=np.full(K,np.nan),where=n1>0)
t['rate_change']=t.July_raw_rate-t.early_raw_rate
t.to_csv(OUT/'covered_sender_stability.csv',index=False)
stable=t[(t.early_n>=1000)&(t.July_n>=1000)]
summary={'fixed_alpha':alpha,'early_n':int(early.sum()),'July_n':int((~early).sum()),'constant_July_nll':nll(constant),'sender_July_nll':nll(pred),'gain_nats':nll(constant)-nll(pred),'July_unknown_sender_n':int(n1[n0==0].sum()),'stable_cells':len(stable),'stable_rate_range_early':[float(stable.early_raw_rate.min()),float(stable.early_raw_rate.max())],'stable_weighted_absolute_rate_change':float(np.average(stable.rate_change.abs(),weights=stable.July_n)),'stable_rate_correlation':float(stable.early_raw_rate.corr(stable.July_raw_rate))}
(OUT/'covered_sender_independent_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2));print(t.sort_values('early_n',ascending=False).head(25).to_string(index=False))
print('Shared B cache, independently implemented np.bincount model; alpha100 fixed before calculation, no July alpha selection.')
