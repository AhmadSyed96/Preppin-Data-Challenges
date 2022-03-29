import pandas as pd
from pandasgui import show
import numpy as np

#load the dataset
df_winners =  pd.read_excel('USOpenWinners.xlsx').rename(columns={'year':'Year'})
df_prize_money = pd.read_excel('Location Prize Money.xlsx')
df_output = pd.merge(df_winners, df_prize_money, how='left', on='Year')

#add in the needed columnns
df_output['to par'] = pd.to_numeric(df_output['to par'], errors='coerce').fillna(0)
df_output['Par Score'] = df_output['total'] - df_output['to par']
df_output['Round Par Score'] = (df_output['Par Score']/4).round(decimals=0)

#pivot the rounds columns into one
rounds = ['round 1', 'round 2', 'round 3', 'round 4']
numbers=[1,2,3,4]
ids = df_output.drop(columns = rounds).columns.to_list()
df_output = df_output.melt(id_vars=ids, value_vars=rounds, value_name='Round Score', var_name='Round').replace(dict(zip(rounds, numbers)))

#union 3 times
df_output['table'] = 1
df_output2 = df_output.assign(table=2)
df_output3 = df_output.assign(table=3)
df_output4 = df_output.assign(table=4)
df_output = pd.concat([df_output2,df_output3,df_output4])

#add round score compared to par score
df_output['Round to Par'] = df_output['Round Score'] - df_output['Round Par Score']

#create round result type
df_output['Round Result Type'] = np.where(df_output['Round Score'] > df_output['Round Par Score'], 'over', np.where(df_output['Round Score'] < df_output['Round Par Score'], 'under', 'par'))

#add square color
df_output['Square Color'] = df_output['Round'].map({1:'A', 2:'B', 3:'C', 4:'D'})

#create side len
df_output['Side Len'] = df_output['Round Score'] ** (1/2)

#add x coor
A = df_output['Square Color'] == 'A'
B = df_output['Square Color'] == 'B'
C = df_output['Square Color'] == 'C'
D = df_output['Square Color'] == 'D'
t1 = df_output['table'] == 1
t2 = df_output['table'] == 2
t3 = df_output['table'] == 3
t4 = df_output['table'] == 4
val1 = np.where(t1,df_output['Side Len'], np.where(t2,0,np.where(t3,0,np.where(t4, df_output['Side Len'],0))))
val2 = np.where(t1, 0, np.where(t2, df_output['Side Len'], np.where(t3, df_output['Side Len'], np.where(t4, 0, 0))))
val3 = np.where(t1, 0, np.where(t2, 0, np.where(t3, df_output['Side Len'], np.where(t4, df_output['Side Len'], 0))))
val4 = np.where(t1, df_output['Side Len'], np.where(t2, df_output['Side Len'], np.where(t3, 0, np.where(t4, 0, 0))))

df_output['x coor'] = np.where(A, val1, np.where(B, val1, np.where(C, val2, np.where(D, val2, 0))))
df_output['y coor'] = np.where(A, val3, np.where(B, val4, np.where(C, val4, np.where(D, val3, 0))))

#create the decade
df_output['Decade'] = (df_output['Year']//10)*10

#create a rank of decade and that years last digit + 1
df_output['Decade Rank'] = df_output['Decade'].rank(method='dense')
df_output['Year of Decade'] =  (df_output['Year'].astype('string').str[-1]).astype('int')

#get output 2
df_output_2 = df_output.groupby('Decade', as_index=False).agg(Max_Tot = ('total', 'sum'), Min_Tot = ('total', 'min'), Max_Score = ('Round Score', 'max'), Min_Score = ('Round Score', 'min'))
show(df_output_2)





