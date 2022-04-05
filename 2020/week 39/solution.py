import pandas as pd
from pandasgui import show
from fuzzywuzzy import process
import numpy as np

cols = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df_orders =   pd.read_excel('2020W39 Input (1).xlsx', sheet_name='Orders')\
                .replace(' with', ',', regex=True)\
                .replace(np.nan, '')\
                .assign(orders = lambda dfx : dfx.loc[:,dfx.columns != 'Person'].apply(lambda x : ', '.join(x), axis=1))\
                .assign(orders = lambda dfx : dfx['orders'].str.split(', '))\
                .explode('orders')\
                .drop(columns=cols)\
                .replace('', np.nan)\
                .dropna()

df_prices = pd.read_excel('2020W39 Input (1).xlsx', sheet_name='Price List')
df_prices =   pd.concat([df_prices.iloc[:, ::2].melt(),
                            df_prices.iloc[:, 1::2].melt()],
                            axis=1)\
                .dropna()\
                .set_axis(['Category', 'Subcategory', 'variable_2', 'Price'],
                            axis='columns')\
                .drop(columns='variable_2')

for item in df_prices['Subcategory']:
    matches = process.extract(item, df_orders['orders'], limit=len(df_orders['orders']))

    for match in matches:
        if match[1] >= 90:
            df_orders['orders'].loc[df_orders['orders'] == match[0]] = item
print(df_orders['orders'].unique())
# show(df_orders)

df_output = pd.merge(df_prices, df_orders, left_on='Subcategory', right_on='orders').groupby('Person', as_index=False)['Price'].sum().assign(Price = lambda dfx : dfx['Price']*4, savings = lambda dfx :dfx['Price'] - 20, Worthwhile = lambda dfx : dfx['savings'] > 0)
show(df_output)