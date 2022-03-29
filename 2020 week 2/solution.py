import pandas as pd
import numpy as np

df = pd.read_csv('PD 2020 Wk 2 Input - Time Inputs.csv')
# print(df)

df["numbers"] = df.Time.str.replace('[^\d+]', '')
# print(df)

df['num len'] = df.numbers.apply(lambda x : len(x))
# print(df)

df['numbers'] = np.where(df['num len']==3,'0'+df['numbers'],df['numbers'])
# print(df)

df.loc[df.Time.str.contains('a',case=False),'AM/PM']='AM'
df.loc[df.Time.str.contains('p',case=False),'AM/PM']='PM'
# print(df)

df['Hour'] = df.numbers.apply(lambda x : x[0:2]).astype('int')
df['Minute'] = df.numbers.apply(lambda x : x[2:]).astype('int')
# print(df)

df['Hour'] = np.where(df['AM/PM']=='PM',df['Hour']+12,df.Hour)
df['Hour'] = np.where(((df['AM/PM']=='AM')&(df['Hour']==12)),df['Hour']*0,df['Hour'])
# print(df)

df['New Time'] = df.Hour.astype('string') + ':' + df.Minute.astype('string') + ':00'
# print(df)

# df['New Time'] = df['New Time'].astype('time')
df['Date Time'] = df['Date'] + ' ' + df['New Time']
# print(df)

df['Date Time'] = pd.to_datetime(df['Date Time'])
# print(df)

df = df[['Date Time']]
print(df)