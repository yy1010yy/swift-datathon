"""Small dependency-free charts sourced from executed aggregate tables."""
from pathlib import Path
from html import escape
import pandas as pd
base=Path(__file__).resolve().parent;out=base/'charts';out.mkdir(exist_ok=True)
def bars(name,title,note,labels,values,unit):
    h=145+44*len(values);m=max(values) or 1
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="{h}">',
       '<rect width="100%" height="100%" fill="white"/><g font-family="Arial" fill="#183746">',
       f'<text x="24" y="32" font-size="22">{escape(title)}</text>',
       f'<text x="24" y="62" font-size="13">{escape(note)}</text>']
    for i,(lab,v) in enumerate(zip(labels,values)):
        y=88+44*i
        s.extend([f'<text x="24" y="{y+20}" font-size="14">{escape(str(lab))}</text>',
          f'<rect x="310" y="{y}" width="{v/m*600:.3f}" height="27" fill="#247d83"/>',
          f'<text x="{320+v/m*600:.3f}" y="{y+20}" font-size="14">{v:,.3g}</text>'])
    s.extend([f'<text x="24" y="{h-18}" font-size="13">{escape(unit)}; zero baseline; supplied synthetic payments only.</text>','</g></svg>'])
    (out/name).write_text('\n'.join(s),encoding='utf-8');print('Saved',name)

a=pd.read_csv(base/'b/amount_unlabeled_currency_party_period.csv').query("currency=='USD'").sort_values(['party','period'])
bars('V2_amounts.svg','Business roles shift typical payment sizes upward',
     'USD currency only; no recorded anomaly label; before July vs July 2023. Medians, not exact universal multipliers.',
     [f'{r.party} / {r.period} (n={r.n:,})' for r in a.itertuples()],a['median'].tolist(),'Median normalized USD amount')
h=pd.read_csv(base/'c/history_summary.csv',keep_default_na=False).set_index('label')
bars('A2_duplicates.svg','Labeled duplicates often copy an earlier amount on the same pair',
     'Strict earlier timestamp, same sender/recipient/currency; controls are selected pairs, not population-random.',
     [f"Duplicate label (eligible n={h.loc['DUPLICATE_PAYMENT','with_prior']:,})",
      f"Blank label (eligible n={h.loc['','with_prior']:,})"],
     [100*h.loc[l,'exact_prior']/h.loc[l,'with_prior'] for l in ['DUPLICATE_PAYMENT','']],
     'Percent with exact preceding amount among records with usable prior history')
d=pd.read_csv(base/'a/duration_model_scores.csv').query('route==0 and participants==2')
bars('D2_duration_models.svg','Two delay groups fit better; exact delay rule remains unresolved',
     'Continuous Direct, 2 visible participants. Fit earlier dates, score July. Lower score is better.',
     d.model.tolist(),d.july_nll_nats.tolist(),'July mean negative log-likelihood, nats per payment')
p=pd.read_csv(base/'text/patterns.csv',keep_default_na=False)
v=[];labs=[]
for side in ['ordering','beneficiary']:
    g=p[p.side.eq(side)&p.feature.eq('country_matches_bank')]
    n=int(g.records.sum());same=int(g.loc[g.value.eq('True'),'records'].sum())
    labs.append(f'{side} (token present n={n:,})');v.append(100*same/n)
bars('X2_country_tokens.svg','Sender country token aligns with bank code; recipient usually differs',
     'Token country compared with corresponding BIC characters 5–6; missing tokens excluded explicitly.',
     labs,v,'Percent matching corresponding bank country code')
