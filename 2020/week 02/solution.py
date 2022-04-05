import pandas as pd
import numpy as np

df = pd.read_csv('PD 2020 Wk 2 Input - Time Inputs.csv')

df["numbers"] = df.Time.str.replace('[^\d+]', '')

df['num len'] = df.numbers.apply(lambda x : len(x))

df['numbers'] = np.where(df['num len']==3,'0'+df['numbers'],df['numbers'])

df.loc[df.Time.str.contains('a',case=False),'AM/PM']='AM'
df.loc[df.Time.str.contains('p',case=False),'AM/PM']='PM'

df['Hour'] = df.numbers.apply(lambda x : x[0:2]).astype('int')
df['Minute'] = df.numbers.apply(lambda x : x[2:]).astype('int')

df['Hour'] = np.where(df['AM/PM']=='PM',df['Hour']+12,df.Hour)
df['Hour'] = np.where(((df['AM/PM']=='AM')&(df['Hour']==12)),df['Hour']*0,df['Hour'])

df['New Time'] = df.Hour.astype('string') + ':' + df.Minute.astype('string') + ':00'

df['Date Time'] = df['Date'] + ' ' + df['New Time']

df['Date Time'] = pd.to_datetime(df['Date Time'])

df = df[['Date Time']]
