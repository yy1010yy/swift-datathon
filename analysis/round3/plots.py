"""Dependency-free SVG evidence charts from saved round-3 result tables."""
from pathlib import Path
from html import escape
import json,pandas as pd

P=Path(__file__).resolve().parent;CH=P/'charts';CH.mkdir(exist_ok=True)
def bars(name,title,note,labels,values,unit,color='#247d83'):
    h=145+44*len(values);m=max(values) or 1
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="{h}">',
       '<rect width="100%" height="100%" fill="white"/><g font-family="Arial" fill="#183746">',
       f'<text x="24" y="32" font-size="22">{escape(title)}</text>',f'<text x="24" y="62" font-size="13">{escape(note)}</text>']
    for i,(lab,v) in enumerate(zip(labels,values)):
        y=88+44*i;w=v/m*600
        s += [f'<text x="24" y="{y+20}" font-size="14">{escape(str(lab))}</text>',
              f'<rect x="390" y="{y}" width="{w:.3f}" height="27" fill="{color}"/>',
              f'<text x="{400+w:.3f}" y="{y+20}" font-size="14">{v:,.4g}</text>']
    s += [f'<text x="24" y="{h-18}" font-size="13">{escape(unit)}; supplied synthetic payments only.</text>','</g></svg>']
    (CH/name).write_text('\n'.join(s),encoding='utf-8');print('Saved',name)

c=pd.read_csv(P/'b/covered_bank_models.csv');models=['global','sender_country','sender_bic','bic_pair'];labels=['Global','Sender country','Sender BIC','Directed BIC pair'];vals=[]
for m in models:
    row=c[c.model.eq(m)].iloc[0] if m=='global' else c[(c.model.eq(m))&(c.alpha.eq(10))].iloc[0];vals.append(row.test_nll)
bars('B3_covered_corridor.svg','Covered vs Indirect is largely a bank-corridor rule','Fit before July; score 1,065,699 July non-Direct payments. Lower is better.',labels,vals,'July negative log loss')

a=json.loads((P/'b/activity_independence.json').read_text());vals=[a['poisson_activity_expected_repeated_pairs_conditional_observed'],a['actual_repeated_pairs']]
bars('N3_pair_recurrence.svg','Endpoint activity alone cannot explain repeat relationships','Observed sender/receiver volumes retained in the diagnostic benchmark.',['Activity-only expectation','Observed'],vals,'Repeated directed account pairs',color='#b33a3a')

d=pd.read_csv(P/'d/anomaly_summary.csv');names=['ACCOUNT_REPLACEMENT_SCAM','CEO_SCAM','CUSTOMER_RECALL'];short=['Replacement','CEO','Recall'];labs=[];vals=[]
for name,label in zip(names,short):
    for role in ['target','control']:
        r=d[(d.label.eq(name))&(d.role.eq(role))].iloc[0];labs.append(f'{label} {role} (n={r.n:,})');vals.append(100*r.account_seen/r.n)
bars('A6_recipient_novelty.svg','Replacement and CEO introduce almost entirely new recipients','Strictly earlier same-sender/currency account history; controls are selected earlier blank payments.',labs,vals,'Percent whose recipient account was seen previously',color='#a63603')

dur=pd.read_csv(P/'c/duration_model_scores.csv');ms=['route+participants+fx','base+sender_receiver_country','base+sender_receiver_bic','base+bics+hour+pair'];labs=['Route / participants / FX','+ endpoint countries','+ endpoint BICs','+ directed BIC pair'];vals=[float(dur[dur.model.eq(m)].log_r2.iloc[0]) for m in ms]
bars('D3_duration.svg','Endpoint banks and corridor explain duration location','Fit May–June complete dates; score 2,896,968 July rows on log duration.',labs,vals,'July log-duration R-squared')

cur=pd.read_csv(P/'c/currency_model_scores.csv');r=cur[cur.model.eq('sender_country')].iloc[0]
bars('C3_currency_menu.svg','Three sender-country choices cover most payment currencies','Earlier sender-country ranked currencies frozen and evaluated on complete-date July.',['Top 1','Top 2','Top 3'],[r.top1_accuracy_all,r.top2_accuracy_all,r.top3_accuracy_all],'Fraction of July payments covered')
print('WROTE',len(list(CH.glob('*.svg'))),'round3 SVG charts')
