import pandas as pd
from pandasgui import show
import numpy as np

df_GBP_rates = pd.read_excel('Attendee List (1).xlsx', sheet_name='Exchange Rates').assign(Currency = lambda dfx : dfx['Currency'].str[:3]).drop(columns=['GBP'])
df_managers = pd.read_excel('Attendee List (1).xlsx', sheet_name='Account Manager')
df_attendents = pd.read_excel('Attendee List (1).xlsx', sheet_name='Attendee List').assign(Company = lambda dfx : dfx['Email'].str.title().str.extract('.*\@(\w*).*'), Currency = lambda dfx : np.where(dfx['Country']=='Mexico', 'MXN', np.where(dfx['Country']=='United States', 'USD', np.where(dfx['Country']=='Canada', 'CAD', 'EUR'))))

df_output_1 = df_attendents.merge(df_managers, how='left', left_on='Company',  right_on='Company List').merge(df_GBP_rates, how='left', on='Currency').assign(Tick_Price_Local = lambda dfx : dfx['Ticket Price (£)'] * dfx['Rate'])
df_output_2 = df_output_1.assign(Tick_Price_Local = lambda dfx : np.where(dfx['Refund Type'] == 'Full Refund', -1 * dfx['Tick_Price_Local'], dfx['Tick_Price_Local'])).groupby(['Currency', 'Country'])['Tick_Price_Local'].sum()
show(df_output_2)