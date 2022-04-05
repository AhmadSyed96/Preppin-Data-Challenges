import pandas as pd
from pandasgui import show
import datetime as dt

df_sales = pd.read_excel('2020W33 (1).xlsx', sheet_name='Daily Sales').assign(adjustment = lambda dfx : dfx['Date'] - dt.timedelta(days=2), Week_of = lambda dfx : dfx['adjustment'].dt.to_period('W').dt.to_timestamp() + dt.timedelta(days=2))
df_orders = pd.read_excel('2020W33 (1).xlsx', sheet_name='Orders').rename(columns={'Date':'Week of Order'})
df_pricing = pd.read_excel('2020W33 (1).xlsx', sheet_name='Scent')

df_output =   pd.merge(df_sales, df_pricing, how='left', on='Scent Code')\
                .assign(Units_Sold = lambda dfx : dfx['Daily Sales'] / dfx['Price'],
                        COGS = lambda dfx : dfx['Units_Sold'] * dfx['Cost'])\
                .groupby(['Week_of', 'Scent'], as_index=False).agg({'Units_Sold':'sum', 'COGS':'sum', 'Daily Sales':'sum', 'Cost':'min'})\
                .rename(columns={'Daily Sales':'Sales'})\
                .merge(df_orders, how='left', left_on='Week_of', right_on='Week of Order')\
                .drop(columns=['Week of Order'])\
                .assign(Waste = lambda dfx : dfx['Units Ordered'] - dfx['Units_Sold'],
                        Waste_Cost = lambda dfx : dfx['Waste'] * dfx['Cost'],
                        Profit = lambda dfx : dfx['Sales'] - dfx['Waste_Cost'])\
                .groupby('Scent')['Profit'].sum()
show(df_output)