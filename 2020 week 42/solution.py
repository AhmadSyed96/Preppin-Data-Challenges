import pandas as pd
from pandasgui import show


df_transactions = pd.read_excel('Transactions (1).xlsx')\
                    .assign(Year = lambda dfx : dfx['TransactionDate'].dt.year,
                            Week=lambda dfx: dfx['TransactionDate'].dt.week)\
                    .drop(columns=['TransactionDate', 'ProductID', 'Price'])\
                    .melt(id_vars=['ProductName', 'Year', 'Week'], value_vars=['Quantity', 'Income'], value_name='This Year', var_name='Metric')
df_transactions_yearly = df_transactions.groupby(['ProductName', 'Metric', 'Year'], as_index=False)['This Year'].sum().assign(Last_Year = lambda dfx : dfx.groupby(['ProductName', 'Metric'])['This Year'].shift(), Time_Period = 'YTD').rename(columns= lambda x : x.replace('_', ' '))
df_transactions_weekly = df_transactions.groupby(['ProductName', 'Metric', 'Year', 'Week'], as_index=False)['This Year'].sum().assign(Last_Year = lambda dfx : dfx.groupby(['ProductName', 'Metric', 'Week'])['This Year'].shift(), Time_Period = 'WTD').rename(columns= lambda x : x.replace('_', ' '))

df_targets =   pd.read_excel('Targets.xlsx').rename(columns={'Quantity Target':'Quantity', 'Income Target':'Income'}).melt(id_vars=['ProductName', 'Year', 'Week'], value_vars=['Quantity', 'Income'], value_name='Target', var_name='Metric')
df_targets_yearly = df_targets.groupby(['ProductName', 'Metric', 'Year'], as_index=False)['Target'].sum().assign(Time_Period = 'YTD').rename(columns= lambda x : x.replace('_', ' '))
df_targets_weekly = df_targets.assign(Time_Period = 'WTD').rename(columns= lambda x : x.replace('_', ' '))
# show(df_targets_yearly, df_transactions_yearly, df_targets_weekly, df_transactions_weekly)

df_weekly_comparison = pd.merge(df_targets_weekly, df_transactions_weekly.query('Year == 2020'), how='right', on=['ProductName', 'Metric', 'Year', 'Week', 'Time Period']).drop(columns=['Year', 'Week'])
df_yearly_comparison = pd.merge(df_targets_yearly, df_transactions_yearly.query('Year == 2020'), how='right', on=['ProductName', 'Metric', 'Year', 'Time Period']).drop(columns=['Year'])
# show(df_weekly_comparison, df_yearly_comparison)

df_output = pd.concat([df_yearly_comparison, df_weekly_comparison]).assign(per_diff_to_last = lambda dfx : (dfx['This Year'] - dfx['Last Year']) / dfx['Last Year'], per_diff_to_target = lambda dfx : (dfx['This Year'] - dfx['Target']) / dfx['Target'])
# show(df_output)



df_transactions_per_day = pd\
                        .read_excel('Transactions (1).xlsx')\
                        .melt(id_vars=['TransactionDate', 'ProductName'], value_vars=['Quantity', 'Income'], value_name='This Year', var_name='Metric')\
                        .assign(Year = lambda dfx : dfx['TransactionDate'].dt.year,
                                Week = lambda dfx : dfx['TransactionDate'].dt.week,
                                YTD = lambda dfx : dfx.groupby(['ProductName', 'Year', 'Metric'])['This Year'].cumsum(),
                                WTD = lambda dfx : dfx.groupby(['ProductName', 'Year', 'Week', 'Metric'])['This Year'].cumsum())\
                        .melt(id_vars=['TransactionDate', 'ProductName', 'Metric'], value_vars=['YTD', 'WTD'], value_name='This Year', var_name='Time Period')\
                        .assign(last_year = lambda dfx : dfx['TransactionDate'] - pd.DateOffset(years=1))

df_transactions_per_day =  df_transactions_per_day.merge(df_transactions_per_day[['TransactionDate',
                                                                'ProductName',
                                                                'Metric',
                                                                'Time Period',
                                                                'This Year']],
                                                how='left',
                                                left_on=['last_year', 'ProductName', 'Metric', 'Time Period'],
                                                right_on=['TransactionDate', 'ProductName', 'Metric', 'Time Period'])\
                                        .drop(columns=['last_year', 'TransactionDate_y'])\
                                        .rename(columns={'TransactionDate_x':'TransactionDate', 'This Year_x':'This Year', 'This Year_y':'Last Year'})\
                                        .assign(Year = lambda dfx : dfx['TransactionDate'].dt.year,
                                                Week = lambda dfx : dfx['TransactionDate'].dt.week)
# show(df_transactions_per_day)

