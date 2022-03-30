import pandas as pd
from pandasgui import show
import numpy as np

df_sales = pd.read_excel('Prep Air Ticket Sales.xlsx', sheet_name='Ticket Sales')\
             .rename(columns={'Value':'Q1 Sales'})
df_targets = pd.read_excel('Prep Air Ticket Sales.xlsx', sheet_name='Sales Target')\
               .rename(columns={'Value':'Q1 Target'})
df_airports = pd.read_excel('Prep Air Ticket Sales.xlsx', sheet_name='Airports')\
                .drop(columns=['Airport'])
df_projections = pd.read_excel('Prep Air Ticket Sales.xlsx', sheet_name='2020 Projections')\
                   .melt(id_vars='Country',
                         value_vars=['Q1-Q2 change %', 'Q1-Q3 change %', 'Q1-Q4 change %'],
                         value_name='% Change from Q1',
                         var_name='Quarter')\
                   .replace({'Q1-Q2 change %':'Q2', 'Q1-Q3 change %':'Q3', 'Q1-Q4 change %':'Q4'})\
                   .assign(number = lambda dfx : dfx['% Change from Q1'].str.extract('(\d+)').astype('int'),
                           sign = lambda dfx : np.where(dfx['% Change from Q1'].str.contains('Minus'), -1, 1),
                           Change = lambda dfx : (dfx['number'] * dfx['sign'] * 0.01) + 1)\
                   .drop(columns=['% Change from Q1', 'number', 'sign'])\
                   .pivot(index='Country', columns='Quarter', values='Change').reset_index().rename_axis(None, axis=1)

df_output = pd.merge(df_sales, df_targets, on=['Date', 'Origin', 'Destination']).merge(df_airports, how='left', left_on='Origin', right_on='Airport Code')\
              .merge(df_airports, how='left', left_on='Destination', right_on='Airport Code')\
              .drop(columns=['Airport Code_x', 'Airport Code_y'])\
              .rename(columns={'Country_x':'Origin Country', 'Country_y':'Destination Country'})\
              .groupby(['Origin', 'Origin Country', 'Destination', 'Destination Country'], as_index=False).agg({'Q1 Sales':'sum', 'Q1 Target':'sum'})\
              .merge(df_projections, how='left', left_on='Destination Country', right_on='Country')\
              .assign(Q2_Sales = lambda dfx: dfx['Q1 Sales'] * dfx['Q2'],
                      Q2_Target = lambda dfx: dfx['Q1 Target'] * dfx['Q2'],
                      Q3_Sales = lambda dfx: dfx['Q1 Sales'] * dfx['Q3'],
                      Q3_Target = lambda dfx: dfx['Q1 Target'] * dfx['Q3'],
                      Q4_Sales = lambda dfx: dfx['Q1 Sales'] * dfx['Q4'],
                      Q4_Target = lambda dfx: dfx['Q1 Target'] * dfx['Q4'])\
              .rename(columns = lambda x : x.replace('_', ' '))\
              .assign(Sales = lambda dfx : dfx['Q1 Sales'] + dfx['Q2 Sales'] + dfx['Q3 Sales'] + dfx['Q4 Sales'],
                      Target = lambda dfx : dfx['Q1 Target'] + dfx['Q2 Target'] + dfx['Q3 Target'] + dfx['Q4 Target'],
                      Variance = lambda dfx : dfx['Sales'] - dfx['Target'])[['Origin', 'Destination', 'Sales', 'Target', 'Variance']]
