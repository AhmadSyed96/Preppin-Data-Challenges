import pandas as pd
from pandasgui import show
import datetime as dt

df_output_1 = pd.read_excel('Medals PD WOW (1).xlsx', sheet_name='Hosts').assign(Year = lambda dfx : pd.to_datetime(dfx['Start Date'], infer_datetime_format=True).dt.year, Host_City = lambda dfx: dfx['Host'].str.extract('(.*)\,.*'), Host_Country = lambda dfx: dfx['Host'].str.extract('.*\,(.*)'))

df_output_2 = pd.read_excel('Medals PD WOW (1).xlsx', sheet_name='Medallists')\
                .groupby(['Country Code', 'Year','Medal'], as_index=False).agg(Count=('Athlete','count'))\
                .pivot(index=['Country Code', 'Year'], columns='Medal', values='Count').reset_index().rename_axis(None, axis=1)

show(df_output_2)