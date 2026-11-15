"""Post-exchange same-population verification, not an independent fit."""
from pathlib import Path
import json,numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'analysis/round2/a'
a=pd.read_csv(OUT/'fat_latent_row_evidence.csv');a=a[a.label.eq('FAT_FINGER_MISTAKE')]
c=pd.read_csv(ROOT/'analysis/round2/c/fat_residual_cases.csv')
m=a.merge(c[['source_record','residual']],on='source_record',suffixes=('_a','_c'),validate='one_to_one')
assert len(m)==1940
delta=float(np.abs(m.residual_a-m.residual_c).max());assert delta<1e-10
models=json.loads((ROOT/'analysis/round2/c/fat_latent.json').read_text())['models']
rows=[]
for model in models:
 for early,period in [(True,'early'),(False,'July')]:
  r=m.loc[m.early.eq(early),'residual_c'].to_numpy()
  mu=np.asarray(model['means']);sd=float(model['sd']);weights=np.asarray(model['weights'])
  f=np.exp(-.5*((r[:,None]-mu)/sd)**2)/(sd*np.sqrt(2*np.pi))
  ll=float(np.log(np.maximum(f@weights,1e-300)).mean())
  expected=model[f'{period}_mean_loglik']
  rows.append([model['name'],period,len(r),ll,expected,ll-expected])
table=pd.DataFrame(rows,columns=['model','period','n','A_recomputed_C_loglik','C_saved_loglik','difference'])
assert table.difference.abs().max()<1e-10
table.to_csv(OUT/'fat_latent_common_input_verification.csv',index=False)
print('PASS all1940 row residuals match; maxabsdelta',delta)
print('PASS C likelihoods recomputed using shared exact residuals/sigma; maxabsdelta',float(table.difference.abs().max()))
print('This verifies arithmetic under matched model assumptions; it does not create another independent baseline or validate the normal family.')
