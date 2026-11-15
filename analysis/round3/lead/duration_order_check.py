"""Lead deciding check: exact endpoint-bank duration effects in both fit orders."""
from pathlib import Path
import json, time
import numpy as np, pandas as pd

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
num=np.load(ROOT/'outputs/round2/a/numeric.npy',mmap_mode='r')
bank=np.load(ROOT/'outputs/round3/c/banks.npy',mmap_mode='r')
epoch=num['epoch']; train=(epoch>=1682899200)&(epoch<1688169600); test=(epoch>=1688169600)&(epoch<1690761600)
tr=np.flatnonzero(train);te=np.flatnonzero(test);start=time.monotonic()

def effect(key,residual,idx,alpha):
    k=key[idx].astype('int64');n=int(key.max())+1
    count=np.bincount(k,minlength=n);total=np.bincount(k,weights=residual[idx],minlength=n)
    return total/(count+alpha)

def score(name,pred):
    ytest=np.log(num['duration'][te].astype(float));e=ytest-pred[te]
    return dict(model=name,n=len(te),log_rmse=float(np.sqrt(np.mean(e*e))),
      log_mae=float(np.mean(abs(e))),log_r2=float(1-np.sum(e*e)/np.sum((ytest-ytest.mean())**2)))

y=np.log(num['duration'].astype(float));global_mean=float(y[tr].mean())
basekey=num['route'].astype('int64')*1000+num['p'].astype('int64')*30+num['fx'].astype('int64')
base=global_mean+effect(basekey,y-global_mean,tr,10)[basekey];res=y-base
s=bank['sender'];r=bank['receiver']
se=effect(s,res,tr,100);re=effect(r,res,tr,100)
sender_first=base+se[s];receiver_after=effect(r,y-sender_first,tr,100);sr=sender_first+receiver_after[r]
receiver_first=base+re[r];sender_after=effect(s,y-receiver_first,tr,100);rs=receiver_first+sender_after[s]
rows=[score('base',base),score('sender_only',base+se[s]),score('receiver_only',base+re[r]),
      score('sender_then_receiver',sr),score('receiver_then_sender',rs),score('average_two_orders',(sr+rs)/2)]
frame=pd.DataFrame(rows);frame.to_csv(OUT/'duration_order_scores.csv',index=False)
result={'status':'PASS','train_rows':len(tr),'july_rows':len(te),'scores':rows,
 'max_additive_order_rmse_difference':float(abs(rows[3]['log_rmse']-rows[4]['log_rmse'])),
 'interpretation':'Both endpoints add duration-location information; ordering sensitivity is reported rather than treated as causality.',
 'elapsed_seconds':time.monotonic()-start}
(OUT/'duration_order_verification.json').write_text(json.dumps(result,indent=2))
print(frame.to_string(index=False));print(json.dumps(result,indent=2))
