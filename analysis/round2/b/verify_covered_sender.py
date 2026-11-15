"""Post-debate exact score concordance of independent Covered-choice implementations."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
OUT=Path(__file__).resolve().parent
b=pd.read_csv(OUT/'covered_sender_scores.csv');lead=pd.read_csv(OUT.parent/'covered_predictor_scores.csv')
def canonical(s):return '+'.join(sorted('participants' if v=='p' else v for v in s.split('+')))
b['canonical']=b.model.map(canonical);lead['canonical']=lead.model.map(canonical)
m=b.merge(lead,on=['canonical','alpha'],suffixes=('_b','_lead'),validate='one_to_one')
assert len(m)==len(b)
assert np.allclose(m.nll,m.july_nll,atol=1e-12,rtol=0)
result={'status':'PASS','matched_model_alpha_cells':len(m),'max_abs_nll_difference':float(abs(m.nll-m.july_nll).max()),'inputs':'Independent scorers on shared B full numeric cache'}
(OUT/'covered_sender_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
