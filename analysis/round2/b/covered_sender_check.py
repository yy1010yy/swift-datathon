"""Independent aggregate target encoding of nonDirect routing, fixed smoothing sensitivities."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
a=np.load(ROOT/'outputs/eda_round2/b_rows.npy',mmap_mode='r');a=a[a['route']!=0]
frame=pd.DataFrame({'sender':a['country'].view('u2'),'currency':a['currency'].astype('i4'),
 'p':a['participants'].astype('i4'),'fx':a['fx'].astype('i4'),'party':a['party'].astype('i4'),
 'early':a['epoch']<1688169600,'covered':a['route']==2})
train=frame[frame.early];test=frame[~frame.early];base=float(train.covered.mean());out=[];details=[]
models=[[],['p','fx'],['sender'],['currency'],['sender','fx'],['currency','fx'],['sender','party','fx'],['currency','party','fx']]
for fields in models:
 if fields:
  agg=train.groupby(fields).covered.agg(['sum','count']).reset_index()
  merged=test.groupby(fields).covered.agg(['sum','count']).reset_index().merge(agg,on=fields,how='left',suffixes=('_test','_train'))
 else:merged=pd.DataFrame([dict(sum_test=test.covered.sum(),count_test=len(test),sum_train=train.covered.sum(),count_train=len(train))])
 for alpha in ([0] if not fields else [10,100,1000]):
  pred=(merged.sum_train+alpha*base)/(merged.count_train+alpha);pred=pred.fillna(base).clip(1e-12,1-1e-12)
  n=merged.count_test.sum();pos=merged.sum_test
  score=float(-(pos*np.log(pred)+(merged.count_test-pos)*np.log1p(-pred)).sum()/n)
  out.append(dict(model='+'.join(fields) if fields else 'constant',alpha=alpha,train_n=len(train),test_n=int(n),train_cells=len(agg) if fields else 1,
   unseen_test_records=int(merged.loc[merged.count_train.isna(),'count_test'].sum()),
   rare_test_records_train_lt100=int(merged.loc[merged.count_train.fillna(0)<100,'count_test'].sum()),nll=score,mean_predicted=float(np.average(pred,weights=merged.count_test)),actual=float(pos.sum()/n)))
  if fields==['sender'] and alpha==100:
   for row,prob in zip(merged.itertuples(),pred):
    country=chr(int(row.sender)&255)+chr(int(row.sender)>>8)
    details.append(dict(sender_country_code=country,train_n=row.count_train,train_covered=row.sum_train,test_n=row.count_test,test_covered=row.sum_test,predicted=float(prob)))
s=pd.DataFrame(out);s.to_csv(OUT/'covered_sender_scores.csv',index=False);pd.DataFrame(details).to_csv(OUT/'covered_sender_cells.csv',index=False)
print(s.to_string(index=False));print('EarlierCoveredrate',base)
print('Sensitivityalphasdescriptive;noJulyselectedbestclaim;receivercountry/individualbankabsentfromcache.')
