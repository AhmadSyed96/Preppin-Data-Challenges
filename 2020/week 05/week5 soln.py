import pandas as pd
from pandasgui import show

df = pd.read_csv('PD 2020 Wk 5 Input (1).csv')
# show(df)

df = df[(df['HTf'] != '-') & (df['HTa'] != '-')]
# show(df)

print(df.columns.values)
df['Rank'] = df['Diff'].rank(method='min', ascending=False)
# show(df)

rank_per_venue = df.groupby('Venue').agg({'Rank' : [('Count', 'count'), ('Best', 'min'), ('Worst', 'max'), ('Avergae', 'mean')]})
# show(rank_per_venue)

