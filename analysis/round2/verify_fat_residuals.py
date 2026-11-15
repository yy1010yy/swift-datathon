"""Reconcile independent adjusted FAT residuals, preserving model differences."""
from pathlib import Path
import json,numpy as np,pandas as pd
p=Path(__file__).resolve().parent
a=pd.read_csv(p/'a/fat_latent_row_evidence.csv',keep_default_na=False)
a=a[a.label.eq('FAT_FINGER_MISTAKE')].set_index('source_record').sort_index()
c=pd.read_csv(p/'c/fat_residual_cases.csv').set_index('source_record').sort_index()
assert len(a)==len(c)==1940
pd.testing.assert_index_equal(a.index,c.index)
np.testing.assert_allclose(a.residual,c.residual,rtol=1e-10,atol=1e-9)
assert (a.early.to_numpy()==c.period.eq('early').to_numpy()).all()
result={'status':'PASS','matched_records':len(a),'early':int(a.early.sum()),
 'july':int((~a.early).sum()),'max_abs_residual_difference':float(np.max(abs(a.residual-c.residual))),
 'limitations':['A uses currency-specific baseline SD; C uses pooled SD, so model likelihoods differ.',
 'Independent initial estimates on same underlying dataset; latent intended amounts and mixture weights remain unobserved.',
 'A/C debate reconciles same-input likelihoods; exact shift powers and weights remain unresolved.']}
(p/'fat_residual_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
