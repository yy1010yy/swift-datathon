"""C temporal-predecessor audit and early-fitted July distribution checks."""
from pathlib import Path
from math import erf,sqrt,log
import pandas as pd
import numpy as np
import json
P=Path(__file__).resolve().parent
h=pd.read_csv(P/'relevant_pair_history.csv.gz',dtype=str,keep_default_na=False)
h['_t']=h.epoch_seconds.astype('int64');h['_row']=h.source_record.astype('int64')
h['_c']=np.rint(pd.to_numeric(h.usd_amount)*100).astype('int64')
records=[]
for _,g in h.groupby(['ordering_account','beneficiary_account','currency_code'],sort=False):
    g=g.sort_values(['_t','_row']);t=g._t.to_numpy();d=g.to_dict('records')
    for i,r in enumerate(d):
        if r['anomaly_type']!='ROMANCE_SCAM':continue
        ix=np.flatnonzero(t<t[i])
        if not len(ix):continue
        # No actual order is observed among tied prior timestamps. For primary
        # cross-review reproducibility select the largest numeric source record.
        j=ix[np.flatnonzero(t[ix]==t[ix].max())[-1]]
        records.append(dict(source_record=r['source_record'],prior_record=d[j]['source_record'],
          prior_label=d[j]['anomaly_type'],period='early' if t[i]<1688169600 else 'July',
          lag=int(t[i]-t[j]),ratio=r['_c']/d[j]['_c']))
e=pd.DataFrame(records);e.to_csv(P/'romance_predecessors.csv',index=False)
early=e[e.period.eq('early')];late=e[e.period.eq('July')]
mu=float(np.log(early.ratio).mean());sd=float(np.log(early.ratio).std(ddof=0));wait=float(early.lag.mean())
checks=[]
def cdfnorm(x):return 0.5*(1+erf((x-mu)/(sd*sqrt(2))))
for name,values,edges,cdf in [
 ('wait_seconds',late.lag,[0,60,120,300,600,1200,np.inf],lambda x:1-np.exp(-x/wait)),
 ('log_amount_ratio',np.log(late.ratio),[-np.inf,0,log(1.5),log(2),log(3),np.inf],cdfnorm)]:
    hist=np.histogram(values,bins=edges)[0]
    for left,right,observed in zip(edges[:-1],edges[1:],hist):
        expected=len(late)*(cdf(right)-cdf(left))
        checks.append(dict(feature=name,left=left,right=right,observed=int(observed),expected=expected,
                         pearson_component=(observed-expected)**2/expected if expected else None))
pd.DataFrame(checks).to_csv(P/'romance_distribution_checks.csv',index=False)
out={'known_history_rows':len(e),'early_rows':len(early),'July_rows':len(late),
     'early_wait_mean':wait,'early_logratio_mean':mu,'early_logratio_sd':sd,
     'prior_labels':e.prior_label.value_counts().to_dict(),
     'July_distribution_discrepancy':pd.DataFrame(checks).groupby('feature').pearson_component.sum().to_dict(),
     'limits':'Retrospective family discovery; grouped dependent sequences; no universal fit or causal proof.'}
(P/'romance_fit.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
