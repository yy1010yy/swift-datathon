"""Post-exchange reconciliation: Jeffreys smoothing for globally unseen July BICs."""
from pathlib import Path
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
a=np.load(ROOT/'outputs/round3/d/intermediaries.npy');tr=a['epoch']<1688169600
rows=[]
for target in ['first','last']:
    K=int(a[target].max())+1;x=np.bincount(a[target][tr],minlength=K).astype(float);y=a[target][~tr].astype(int)
    unseen=x[y]==0; raw=x/x.sum(); smooth=(x+.5)/(x.sum()+.5*K)
    rows.append(dict(target=target,july_n=len(y),unseen_july_rows=int(unseen.sum()),unseen_july_share=float(unseen.mean()),unsmoothed_nll=float(-np.log(np.maximum(raw[y],1e-300)).mean()),jeffreys_nll=float(-np.log(smooth[y]).mean()),top1_accuracy=float((y==int(x.argmax())).mean())))
pd.DataFrame(rows).to_csv(OUT/'intermediary_smoothing_recheck.csv',index=False)
print(pd.DataFrame(rows).to_string(index=False))
