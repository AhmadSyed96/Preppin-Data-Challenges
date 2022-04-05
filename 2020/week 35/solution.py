import pandas as pd
from pandasgui import show

table = pd.read_excel('Input Week 35 (1).xlsx')
columns = [col.replace(' Sales','') for col in table.columns if 'Sales' in str(col)]
stores = table['Store'].dropna().unique()
df = table.iloc[3:,2:].dropna()
sales = df[::3].set_axis(columns, axis=1).assign(Store = stores).melt(id_vars='Store', value_vars=columns, var_name='Month', value_name='Sales')
target = df[1::3].set_axis(columns, axis=1).assign(Store = stores).melt(id_vars='Store', value_vars=columns, var_name='Month', value_name='Target')
# difference = df[2::3].set_axis(columns, axis=1).assign(stores = stores).melt(id_vars='stores', value_vars=columns, var_name='Month', value_name='Sales')

df_output = pd.merge(sales, target, on=['Store', 'Month']).assign(Difference = lambda dfx : dfx['Sales'] - dfx['Target'],
                                                                  Date = lambda dfx : pd.to_datetime('2020'  + dfx['Month'], format='%Y%b'))
show(df_output)