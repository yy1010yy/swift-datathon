from pathlib import Path
import numpy as np,pandas as pd,json
ROOT=Path(__file__).resolve().parents[3]; OUT=ROOT/'analysis/round2/a'
x=np.load(ROOT/'outputs/round2/a/numeric.npy',mmap_mode='r')
amount=x['amount'].copy();duration=x['duration'].copy();part=x['p'].copy();fxv=x['fx'].copy();rt=x['route'].copy();q=x['q'].copy();early=x['epoch'].copy()<1688169600
party=pd.Categorical(x['party'].copy());currency=pd.Categorical(x['currency'].copy());label=pd.Categorical(x['label'].copy())
del x
rows=[]
for period,pm in [('early',early),('july',~early)]:
 for route in range(3):
  for p in np.unique(part[rt==route]):
   for fx in np.unique(fxv[(rt==route)&(part==p)]):
    mask=pm&(rt==route)&(part==p)&(fxv==fx)&(q==1)
    a=duration[mask]
    if len(a):rows.append([period,route,int(p),int(fx),len(a),float(a.mean()),*np.quantile(a,[0,.1,.5,.9,.99,1]).tolist(),float((a<=30*(p-1)).mean())])
pd.DataFrame(rows,columns=['period','route','participants','fx','n','mean','min','p10','median','p90','p99','max','fraction_under_30_per_edge']).to_csv(OUT/'duration_conditional.csv',index=False)
rows=[]
for period,pm in [('early',early),('july',~early)]:
 for route in range(3):
  for continuity in [0,1]:
   for p in np.unique(part[rt==route]):
    a=duration[pm&(rt==route)&(part==p)&(q==continuity)]
    if len(a):rows.append([period,route,continuity,int(p),len(a),float(a.mean()),float(a.var()),*np.quantile(a,[0,.1,.5,.9,.99,1]).tolist(),float((a<100).mean())])
pd.DataFrame(rows,columns=['period','route','continuous','participants','n','mean','variance','min','p10','median','p90','p99','max','fraction_under_100']).to_csv(OUT/'duration_route_participants.csv',index=False)
hist=pd.DataFrame({'route':rt,'p':part,'q':q,'duration':duration}).value_counts(sort=False).rename('n').reset_index()
hist.to_csv(ROOT/'outputs/round2/a/duration_histogram.csv',index=False)
rows=[]
df=pd.DataFrame({'period':early,'party':party,'currency':currency,'amount':amount})
df=df[np.asarray(label=='')]
for keys,g in df.groupby(['period','party','currency'],observed=True):
   period,pa,cu=keys; a=g.amount.to_numpy()
   rows.append(['early' if period else 'july',pa,cu,len(a),*np.quantile(a,[.1,.5,.9,.99]).tolist(),float(np.log10(a).mean()),float(np.log10(a).std()),float((np.round(a*100).astype('i8')%100==0).mean())])
for keys,g in df.groupby(['period','party'],observed=True):
   period,pa=keys;a=g.amount.to_numpy()
   rows.append(['early' if period else 'july',pa,'__ALL_CURRENCIES__',len(a),*np.quantile(a,[.1,.5,.9,.99]).tolist(),float(np.log10(a).mean()),float(np.log10(a).std()),float((np.round(a*100).astype('i8')%100==0).mean())])
pd.DataFrame(rows,columns=['period','party','currency','n','p10','median','p90','p99','mean_log10','std_log10','round_dollar_fraction']).to_csv(OUT/'amount_conditional.csv',index=False)
pd.crosstab(label,party,dropna=False).to_csv(OUT/'label_party.csv')
t=pd.read_csv(OUT/'routing_joint.csv'); y=t[t.q.eq(1)]
print('Continuous fx=countrychanges:',int(y.loc[y.fx.eq(y.changes),'n'].sum()),'/',int(y.n.sum()))
print('FX bound violations:',int(t.loc[t.fx.gt(t.p-1),'n'].sum()))
print('Direct participants:',t[t.route.eq(0)].groupby('p').n.sum().to_dict())
print('Routes participant ranges:',t.groupby('route').p.agg(['min','max']).to_dict())
print('Endpoint flag joint:'); print(t.groupby(['sm','rm']).n.sum())
print('Amounts ALL CURRENCIES:');print(pd.read_csv(OUT/'amount_conditional.csv').query("currency=='__ALL_CURRENCIES__'").to_string(index=False))
print('Durations direct:');print(pd.read_csv(OUT/'duration_conditional.csv').query('route==0').to_string(index=False))
