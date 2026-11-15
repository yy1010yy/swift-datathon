"""Challenge a constant Covered-vs-Indirect draw with conditional predictors."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
a=np.load(ROOT/'outputs/eda_round2/b_rows.npy',mmap_mode='r')
route=a['route'];mask=route!=0;early=a['epoch']<1688169600;y=(route==2).astype('u1')
currency=a['currency'].astype('i4');sender=np.char.decode(a['country'],'ascii')
p=a['participants'].astype('i4');fx=a['fx'].astype('i4');party=a['party'].astype('i4');q=a['continuous'].astype('i4')
base=float(y[mask&early].mean())
def binary_nll(target,prob):
 prob=np.clip(prob,1e-12,1-1e-12);return float(-(target*np.log(prob)+(1-target)*np.log1p(-prob)).mean())
def key_array(fields):
 vals=[]
 for f in fields:
  vals.append({'fx':fx,'participants':p,'currency':currency,'sender':sender,'party':party,'continuous':q}[f])
 return pd.MultiIndex.from_arrays(vals,names=fields) if len(vals)>1 else pd.Index(vals[0],name=fields[0])
models=[[],['fx'],['participants'],['fx','participants'],['currency'],['sender'],['party'],['continuous'],
 ['currency','fx'],['sender','fx'],['currency','party','fx'],['sender','party','fx']]
rows=[];test=mask&~early;train=mask&early
for fields in models:
 for alpha in ([0] if not fields else [10,100,1000]):
  if not fields:pred=np.full(test.sum(),base);cells=1
  else:
   k=key_array(fields);frame=pd.DataFrame({'key':k[train],'y':y[train]})
   agg=frame.groupby('key').y.agg(['sum','count']);rate=(agg['sum']+alpha*base)/(agg['count']+alpha)
   pred=rate.reindex(k[test]).fillna(base).to_numpy();cells=len(agg)
  rows.append(dict(model='+'.join(fields) or 'constant',alpha=alpha,train_n=int(train.sum()),test_n=int(test.sum()),
    cells=cells,july_nll=binary_nll(y[test],pred),july_mean_predicted=float(pred.mean()),july_actual=float(y[test].mean())))
scores=pd.DataFrame(rows);scores.to_csv(OUT/'covered_predictor_scores.csv',index=False)
best=scores.loc[scores.groupby('model').july_nll.idxmin()].sort_values('july_nll')
result={'status':'complete','preJuly_n':int(train.sum()),'July_n':int(test.sum()),
 'preJuly_covered_rate':base,'July_covered_rate':float(y[test].mean()),'best_by_model':best.to_dict('records'),
 'limits':['Predictors are associative; FX and route type may share earlier causes.','Receiver code and individual bank are absent from this cache.','Smoothing compared on July, so best alpha is descriptive.','Rare categories fall back to global earlier rate.']}
(OUT/'covered_predictor_summary.json').write_text(json.dumps(result,indent=2));print(best.to_string(index=False));print(json.dumps({k:v for k,v in result.items() if k!='best_by_model'},indent=2))
