import pandas as pd
from datetime import datetime
from pandasgui import show

with pd.ExcelFile('PD 2020 Wk 8 Input Not Random.xlsx') as xl:
    renames = {'Volume':'Sales Volume', 'Value':'Sales Value'}
    df_weekly = pd.concat([pd.read_excel(xl,s)\
                                              .assign(Week=int(s.replace('Week ', '')))\
                                              .rename(columns=renames) for s in xl.sheet_names if 'Week' in s])\
                          .assign(Type=lambda df_x:df_x['Type'].str.lower())\
                          .groupby(['Week','Type'],as_index=False)[['Sales Value', 'Sales Volume']].sum()
    budget_sheet = pd.read_excel(xl, 'Budget', skiprows=2)\
                     .dropna(how='all', axis=1)\
                     .rename(str.strip, axis=1)
# show(df_weekly)



profit_df = budget_sheet.iloc[0:15, 0:4].assign(Type=lambda df_x: df_x['Type'].str.lower(),
                                                Year=lambda df_x: df_x['Week'].str[0:4],
                                                Week=lambda df_x: df_x['Week'].str[-1:].astype('int'))
# show(profit_df)



budget_df = budget_sheet.iloc[19:, :5].set_axis([c.strftime('%d-%m') if isinstance(c, datetime) else c for c in budget_sheet.iloc[18]], axis=1)\
                                      .melt(id_vars=['Type', 'Measure'], var_name='Week')\
                                      .assign(Type=lambda df_x:df_x['Type'].str.replace('[\d_]','',regex=True).str.lower(),
                                              Start_Week=lambda df_x: df_x['Week'].str[0:2].astype('int'),
                                              End_Week=lambda df_x: df_x['Week'].str[3:].astype('int'),
                                              value=lambda df_x:df_x['value'].astype('float'))\
                                      .pivot_table(index=['Type', 'Start_Week', 'End_Week', 'Week'], values='value',
                                                   columns=['Measure'], aggfunc='sum')\
                                      .reset_index()
budget_df = budget_df.assign(Week=[list(range(i, j+1)) for i, j in budget_df[['Start_Week', 'End_Week']].values])\
                     .explode('Week')
# show(budget_df)



df_filt_profit = pd.merge(df_weekly, profit_df, how='left', on=['Week', 'Type'])
df_filt_profit = df_filt_profit[(df_filt_profit['Sales Value'] > df_filt_profit['Profit Min Sales Value'])&(df_filt_profit['Sales Volume'] > df_filt_profit['Profit Min Sales Volume'])]
# show(df_filt_profit)

df_filt_budget = pd.merge(df_weekly, budget_df, how='left', on=['Week', 'Type'])
# print(df_filt_budget.columns.values)
df_filt_budget = df_filt_budget[(df_filt_budget['Sales Value'] > df_filt_budget['Budget Value'])&(df_filt_budget['Sales Volume'] > df_filt_budget['Budget Volume'])]
show(df_filt_budget)