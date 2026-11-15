"""Post-debate sender-control/currency exact agreement; no new raw-data extraction."""
from pathlib import Path
import json
import pandas as pd
OUT=Path(__file__).resolve().parent
b=pd.read_csv(OUT/'sender_independent_rows.csv');c=pd.read_csv(OUT.parent/'c/sender_controls.csv')
m=b.merge(c,on=['target_record','label','role'],suffixes=('_b','_c'),validate='one_to_one')
assert len(m)==len(b)==len(c)==11615
assert (m.record_b==m.record_c).all() and (m.prior_b==m.prior_c).all()
for col in ['exact_same','exact_different','power_exact']:assert (m[col+'_b']==(m[col+'_c']>0)).all()
b=pd.read_csv(OUT/'currency_temporal_predictions.csv')
sender=int(b.loc[b.predictor.eq('sender_country_mode'),'correct_n'].sum())
receiver=int(b.loc[b.predictor.eq('receiver_country_mode'),'correct_n'].sum())
assert sender==2592753 and receiver==932564
result={'status':'PASS','sender_target_control_rows':len(m),'sender_history_targets':int(m.role.eq('target').sum()),'currency_july_records':int(b.loc[b.predictor.eq('sender_country_mode'),'n'].sum()),
 'sender_currency_correct':sender,'receiver_currency_correct':receiver,
 'checks':['B/C everyselectedcontrolsource andstrictpriorhistorycount',
 'B/C all exactsame/differentreceiver andpower10 target/control indicators',
 'B/C temporal currency-mode prediction exact totals'],
 'notes':['SenderhistoryextractionsharedwithC;scorerindependent.','CurrencycountsBrawextraction;Cindependentlyscoredsharedcounts.']}
(OUT/'extended_review_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
