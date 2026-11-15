"""Temporal stability of blind intermediary marginal distributions."""
from pathlib import Path
import json,numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
a=np.load(ROOT/'outputs/round3/d/intermediaries.npy');train=a['epoch']<1688169600
rows=[]
for target in ['first','last']:
    size=int(a[target].max())+1
    x=np.bincount(a[target][train],minlength=size).astype(float);y=np.bincount(a[target][~train],minlength=size).astype(float)
    xp=x/x.sum();yp=y/y.sum();mask=(x>=100)&(y>=100)
    rows.append(dict(target=target,train_n=int(x.sum()),july_n=int(y.sum()),total_variation=float(np.abs(xp-yp).sum()/2),pearson_rate_correlation=float(np.corrcoef(xp[mask],yp[mask])[0,1]),banks_n_ge_100_both=int(mask.sum()),train_top1_share=float(xp.max()),july_top1_share=float(yp.max())))
pd.DataFrame(rows).to_csv(OUT/'intermediary_stability.csv',index=False)
print(pd.DataFrame(rows).to_string(index=False))
