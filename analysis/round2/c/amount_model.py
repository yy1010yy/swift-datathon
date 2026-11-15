"""Exact row-level OLS from sufficient within-cell log moments, no raw-data rescan."""
from pathlib import Path
import pandas as pd
import numpy as np
import json
P=Path(__file__).resolve().parent
q=pd.read_csv(P/'amount_quantiles.csv');q=q[q.labelled.eq(False)].copy()
train=q[q.period.eq('pre_july')];test=q[q.period.eq('july')]
currencies=sorted(train.currency.unique());lookup={c:i for i,c in enumerate(currencies)}
def design(d):
    X=np.zeros((len(d),len(currencies)+2))
    for i,r in enumerate(d.itertuples()):
        if r.currency in lookup:X[i,lookup[r.currency]]=1
        X[i,-2]=r.party_pair[0]=='B';X[i,-1]=r.party_pair[1]=='B'
    return X
X=design(train);w=np.sqrt(train.n.to_numpy());y=train.mean_log.to_numpy()
beta=np.linalg.lstsq(X*w[:,None],y*w,rcond=None)[0]
grand_mean=np.average(y,weights=train.n)
result={'method':'OLS on exact weighted within-cell natural-log means; within-cell variances retained for full-row errors',
        'training':'all no-recorded-label rows before July1UTC','test':'all no-recorded-label July rows',
        'sender_beta':float(beta[-2]),'receiver_beta':float(beta[-1]),
        'sender_factor':float(np.exp(beta[-2])),'receiver_factor':float(np.exp(beta[-1])),
        'currency_intercepts':dict(zip(currencies,map(float,beta[:-2])))}
for name,d in [('train',train),('july',test)]:
    pred=design(d)@beta;n=d.n.to_numpy();m=d.mean_log.to_numpy();variance=d.sd_log.to_numpy()**2
    sse=np.sum(n*(variance+(m-pred)**2));baseline=np.sum(n*(variance+(m-grand_mean)**2))
    result[name]={'rows':int(n.sum()),'log_rmse':float(np.sqrt(sse/n.sum())),
                  'r2_against_early_mean':float(1-sse/baseline),
                  'r2_against_period_mean':float(1-sse/np.sum(n*(variance+(m-np.average(m,weights=n))**2))),
                  'unseen_currency_rows':int(d.loc[~d.currency.isin(currencies),'n'].sum())}
(P/'amount_model.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='currency_intercepts'},indent=2))
