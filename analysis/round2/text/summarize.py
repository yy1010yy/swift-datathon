from pathlib import Path
import pandas as pd
out=Path(__file__).resolve().parent
p=pd.read_csv(out/'patterns.csv');f=pd.read_csv(out/'families.csv')
for feature in ['line35_token','newline_style','starts_slash','country_token_count','country_matches_bank']:
    print('\nFEATURE',feature)
    print(p[p.feature.eq(feature)].groupby(['side','party','value']).records.sum().to_string())
print('\nTOKEN FAMILIES')
print(f.groupby(['side','party','token_family']).records.sum().to_string())
assert p[p.feature.eq('newline_style')].records.sum()==20000000
print('\nPASS20M fields across10M transactions')
