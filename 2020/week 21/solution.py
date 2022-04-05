import pandas as pd
from pandasgui import show

df_sales = pd.read_csv('2020W21 Input (1).csv')\
             .assign(Month_Number =
                     lambda dfx : dfx['Month'].map({'January': 1, 'Febuary': 2, 'March': 3,
                                                    'April': 4, 'May': 5, 'June': 6, 'July': 7,
                                                    'August': 8, 'September': 9, 'October': 10,
                                                    'November': 11, 'December': 12}))\

df_output_1_2 = df_sales.groupby(['Company', 'Month'], as_index=False)['Sales'].sum()\
                        .pivot(index=['Company'], values=['Sales'], columns=['Month'])\
                        .reset_index()


df_output_1_2.columns = ['_'.join(col) for col in df_output_1_2.columns.values]
df_output_1_2 = df_output_1_2.assign(Total_March = lambda dfx : dfx['Sales_March'].sum(),
                                     Total_April = lambda dfx : dfx['Sales_April'].sum(),
                                     April_Market_Share = lambda dfx : dfx['Sales_April'] / dfx['Total_April'] * 100,
                                     March_Market_Share = lambda dfx : dfx['Sales_March'] / dfx['Total_March'] * 100,
                                     bps_change = lambda dfx : dfx['April_Market_Share'] - dfx['March_Market_Share'],
                                     Growth = lambda dfx : (dfx['Sales_April'] - dfx['Sales_March']) / dfx['Sales_March'] * 100)\
                             .rename(columns = lambda x : x.replace('_', ' '))\
                             .drop(columns=['Total March', 'Total April', 'March Market Share', 'Sales March', 'Sales April'])
show(df_output_1_2)


df_output_2_2 = df_sales.replace({'Sudsie Malone': 'Rest of Market',
                                  'Squeaky Cleanies': 'Rest of Market',
                                  'Soap and Splendour': 'Rest of Market',
                                  'British Soaps': 'Rest of Market'})\
                        .groupby(['Company', 'Soap Scent', 'Month_Number', 'Month'], as_index=False)['Sales'].sum()\
                        .pivot(index=['Company', 'Soap Scent'], values='Sales', columns='Month').reset_index(level=[0,1])\
                        .assign(March_Sales_Total = lambda dfx : dfx.groupby('Company',as_index=False)['March'].sum()\
                                                                    .add_prefix('left_')\
                                                                    .merge(dfx, how='right', left_on='left_Company', right_on='Company')\
                                                                    .reset_index()['left_March'],
                                Contributiion_to_Growth = lambda dfx : (dfx['April'] - dfx['March']) / dfx['March_Sales_Total'] * 100)

show(df_output_2_2)



