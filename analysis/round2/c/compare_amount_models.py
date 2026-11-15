"""Independent sufficient-moment fit vs B's raw-numeric row fit."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent
c=json.loads((P/'amount_model.json').read_text())
b=json.loads((P.parent/'b/amount_scale_models.json').read_text())
checks=[]
for row in b:
    if row['model']!='currency_sender_receiver':continue
    period='july' if row['period']=='July' else 'train'
    assert row['n']==c[period]['rows']
    assert abs(row['rmse_log_amount']-c[period]['log_rmse'])<1e-12
    assert abs(row['r2_log_amount']-c[period]['r2_against_period_mean'])<1e-12
    for role in ['sender','receiver']:
        assert abs(row['params'][role+'_business_log_shift']-c[role+'_beta'])<1e-12
    checks.append(dict(period=period,rows=row['n'],rmse_difference=row['rmse_log_amount']-c[period]['log_rmse'],
       r2_difference=row['r2_log_amount']-c[period]['r2_against_period_mean']))
out={'status':'PASS','checks':checks,'note':'C full-file exact group log moments vs B raw-numeric cache; no unobserved outcome assumptions'}
(P/'amount_model_concordance.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
