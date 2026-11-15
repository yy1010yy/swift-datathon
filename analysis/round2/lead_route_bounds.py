"""Lead's independently computed bounds from existing full-file FX counts."""
from pathlib import Path
import pandas as pd
root=Path(__file__).resolve().parents[2]
d=pd.read_csv(root/'outputs/eda_initial/routing_fx.csv')
assert d.records.sum()==10000000
print('Joint support of FX count by continuity and route:')
print(d.groupby(['continuity','route_type','fx_steps']).records.sum().to_string())
print('\nTest: FX steps cannot exceed participant_count - 1:')
print(d.assign(exceeds=d.fx_steps>d.participant_count-1).groupby(['continuity','route_type','exceeds']).records.sum().to_string())
print('\nParticipant bounds by route:')
print(d.groupby('route_type').participant_count.agg(['min','max']).to_string())
