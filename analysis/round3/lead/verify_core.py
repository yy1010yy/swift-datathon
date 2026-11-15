"""Cross-review verification for completed round-3 bank, currency, duration and entity results."""
from pathlib import Path
import json
import pandas as pd

ROOT=Path(__file__).resolve().parents[3]
A=ROOT/'analysis/round3/a';B=ROOT/'analysis/round3/b';C=ROOT/'analysis/round3/c';OUT=Path(__file__).resolve().parent

av=json.loads((A/'entity_verification.json').read_text())
bv=json.loads((B/'verification.json').read_text())
ba=json.loads((B/'activity_independence.json').read_text())
assert av['status']==bv['status']=='PASS'
assert av['pairs']==bv['observed_pairs']==ba['observed_pairs']==8258480
assert av['payments']==bv['blank_pair_rows']==ba['blank_payments']==9992994
assert ba['actual_repeated_pairs']==628578
assert min(av['observed_over_expected_range'])>3 and ba['ratio_actual_to_expected_repeated_pairs']>3

bc=pd.read_csv(B/'currency_bank_models.csv');cc=pd.read_csv(C/'currency_model_scores.csv')
b_country=bc[(bc.model=='sender_country')&(bc.alpha==100)].iloc[0]
b_bic=bc[(bc.model=='sender_bic')&(bc.alpha==100)].iloc[0]
c_country=cc[cc.model=='sender_country'].iloc[0];c_bic=cc[cc.model=='sender_bic'].iloc[0]
assert abs(b_country.test_accuracy-c_country.top1_accuracy_all)<1e-4
assert b_bic.test_nll>b_country.test_nll
assert c_bic.top1_accuracy_all<=c_country.top1_accuracy_all+1e-5

bd=pd.read_csv(B/'continuous_bank_models.csv');cd=pd.read_csv(C/'duration_model_scores.csv')
b_base=bd[(bd.outcome=='log_duration')&(bd.model=='baseline')].iloc[0]
b_sender=bd[(bd.outcome=='log_duration')&(bd.model=='sender_bic')].iloc[0]
c_base=cd[cd.model=='route+participants+fx'].iloc[0]
c_banks=cd[cd.model=='base+sender_receiver_bic'].iloc[0]
c_pair=cd[cd.model=='base+bics+hour+pair'].iloc[0]
assert abs(b_base.test_rmse-c_base.log_rmse)<1e-3
assert b_sender.test_rmse<b_base.test_rmse*.8
assert c_banks.log_rmse<c_base.log_rmse*.7 and c_pair.log_rmse<c_banks.log_rmse

timing=pd.read_csv(B/'timing_bank_models.csv')
t_country=timing[(timing.model=='sender_country')&(timing.alpha==1000)].iloc[0]
t_bic=timing[(timing.model=='sender_bic')&(timing.alpha==1000)].iloc[0]
assert t_bic.test_nll>t_country.test_nll

result={'status':'PASS','entity':{'blank_rows':9992994,'pairs':8258480,'repeated_pairs':628578,
 'A_activity_null_ratio_range':av['observed_over_expected_range'],'B_full_activity_null_ratio':ba['ratio_actual_to_expected_repeated_pairs']},
 'currency':{'B_july_rows':int(b_country.test_n),'C_complete_july_rows':int(c_country.test_n),
 'B_sender_country_accuracy':b_country.test_accuracy,'C_sender_country_accuracy':c_country.top1_accuracy_all,
 'finding':'Exact sender BIC does not improve the sender-country currency model in either implementation.'},
 'duration':{'baseline_log_rmse':c_base.log_rmse,'B_sender_only_log_rmse':b_sender.test_rmse,
 'C_both_banks_log_rmse':c_banks.log_rmse,'C_pair_log_rmse':c_pair.log_rmse,
 'finding':'Independent implementations agree that exact endpoint banks carry large, stable duration-location effects.'},
 'timing':{'country_nll':t_country.test_nll,'exact_sender_bic_nll':t_bic.test_nll,
 'finding':'Exact bank does not improve sender-country weekly timing prediction.'},
 'population_note':'B includes partial boundary dates for currency/duration; C uses May1-Jun30 and Jul1-30. Near-identical common baselines make this boundary immaterial to direction.'}
(OUT/'core_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
