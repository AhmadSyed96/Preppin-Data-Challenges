import pandas as pd
from pandasgui import show
import numpy as np

#load the dataset
df_new_ranges = pd.read_csv('New Star Signs.csv', names=['Data'], header=None)

#split the columns
df_new_ranges[['Sign', 'Start Month', 'Start Date', 'End Month', 'End Date']] = df_new_ranges['Data'].str.extract('(\w+)\W+(\w+)\s(\w+)\W+(\w+)\s(\w+)')
df_new_ranges['Start Month'] = df_new_ranges['Start Month'].str[:3]
df_new_ranges['End Month'] = df_new_ranges['End Month'].str[:3]
df_new_ranges['New Start'] = df_new_ranges['Start Month'] + ' ' + df_new_ranges['Start Date']
df_new_ranges['New End'] = df_new_ranges['End Month'] + ' ' + df_new_ranges['End Date']

#fix start and end dtypes
df_new_ranges['New Start'] = pd.to_datetime(df_new_ranges['New Start'] + ' 2020', format='%b %d %Y')
df_new_ranges['New End'] = pd.to_datetime(df_new_ranges['New End'] + ' 2020', format='%b %d %Y')

#keep only
df_new_ranges['Date Range'] = df_new_ranges['Data'].str.extract('.*\:\s(.*)')
df_new_ranges = df_new_ranges[['Sign', 'Date Range', 'New Start', 'New End']]


#load the dataset
df_old_signs_unparsed = pd.read_csv('Old Star Signs.csv', names=['Sign 1', 'Date Range 1', 'Sign 2', 'Date Range 2', 'Sign 3', 'Date Range 3'], header=None,skipfooter=1, encoding='utf_8_sig')

#concat the df
col_len = len(df_old_signs_unparsed.columns)
df_old_ranges = None
for i in range(0,col_len,2):
    df = df_old_signs_unparsed.iloc[:,i:i+2]
    df.columns = ['Sign', 'Date Range']
    # print(df)
    df_old_ranges = pd.concat([df_old_ranges, df])

#get the start and end
df_old_ranges['Old Start'] = df_old_ranges['Date Range'].str.extract('(\w+\/\w+)\–.*')
df_old_ranges['Old End'] = df_old_ranges['Date Range'].str.extract('.*\–(\w+\/\w+)')

#convert to date
df_old_ranges['Old Start'] = pd.to_datetime('2020/' + df_old_ranges['Old Start'], format='%Y/%m/%d')
df_old_ranges['Old End'] = pd.to_datetime('2020/' + df_old_ranges['Old End'], format='%Y/%m/%d')

#remove date range
df_old_ranges.drop(columns=['Date Range'], inplace=True)

#add dates and prepare dummy
df_dates = pd.read_csv('Scaffold.csv').assign(dummy = 1, Date = lambda dfx : pd.to_datetime(dfx['Date'], format='%d/%m/%Y'))
df_new_ranges['dummy'] = 1
df_old_ranges['dummy'] = 1

#cross join date with the two other dfs
df_old_signs = pd.merge(df_dates, df_old_ranges, on='dummy')
df_new_signs = pd.merge(df_dates, df_new_ranges, on='dummy')

#find the signs for each date
df_old_signs['Old Sign'] = np.where((df_old_signs['Date'] >= df_old_signs['Old Start']) & (df_old_signs['Date'] <= df_old_signs['Old End']), df_old_signs['Sign'], np.nan)
df_new_signs['New Sign'] = np.where((df_new_signs['Date'] >= df_new_signs['New Start']) & (df_new_signs['Date'] <= df_new_signs['New End']), df_new_signs['Sign'], np.nan)

#drop nans
df_old_signs.dropna(inplace=True)
df_new_signs.dropna(inplace=True)

#keep only
df_old_signs = df_old_signs[['Date', 'Old Sign']]
df_new_signs = df_new_signs[['Date', 'New Sign']]

#join
df_output = pd.merge(df_new_signs, df_old_signs, on='Date')

#get rid of unchanged signs
df_output = df_output[df_output['Old Sign'] != df_output['New Sign']]
show(df_output)