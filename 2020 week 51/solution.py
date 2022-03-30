import pandas as pd
from pandasgui import show
import numpy as np

with pd.ExcelFile('NBA 2018_19 Results - Copy.xlsx') as xl:
    df_games = pd.concat(pd.read_excel(xl, sheet).assign(Date = lambda dfx : pd.to_datetime(dfx['Date'], errors='coerce')) for sheet in xl.sheet_names)
df_games_per_team  = df_games.assign(Team = lambda dfx : dfx[['Visitor/Neutral', 'Home/Neutral']].apply(list, axis=1))\
                             .explode('Team')\
                             .assign(game = lambda dfx : dfx.groupby('Team')['Date'].rank(),
                                     Frm = lambda dfx : dfx.groupby('Team')['Home/Neutral'].shift())\
                             .assign(Frm = lambda dfx : np.where(dfx['Frm'].isnull(), dfx['Team'], dfx['Frm']))\
                             .rename(columns={'Home/Neutral':'To'})\
                             .assign(Frm = lambda dfx : dfx['Frm'].str.replace('\s\w*$','',regex=True),
                                     To = lambda dfx : dfx['To'].str.replace('\s\w*$','',regex=True))\
                             .replace({'Portland Trail':'Portland', 'Oklahoma City':'Oklahoma'})[['Team', 'Frm', 'To']]

df_distances = pd.read_excel('NBA Travel Distances.xlsx')\
                 .rename(columns={'From    To':'Frm'})
cities = df_distances.iloc[:,1:].columns.to_list()
df_distances = df_distances.melt(id_vars='Frm', value_vars=cities, value_name='Distance Time', var_name='To')\
                           .assign(Hours = lambda dfx : dfx['Distance Time'].str.extract('(.*)h.*'),
                                   Minutes = lambda dfx : dfx['Distance Time'].str.extract('(\d+)m'))\
                           .assign(Hours = lambda dfx : dfx['Hours'].fillna(0).astype('int'),
                                   Minutes = lambda dfx : dfx['Minutes'].fillna(0).astype('int'),
                                   Time = lambda dfx : dfx['Hours'] * 60 + dfx['Minutes'])[['Frm', 'To', 'Time']]

df_output = pd.merge(df_distances, df_games_per_team, how='right', on=['Frm', 'To'])\
              .groupby('Team')['Time'].sum()
show(df_output)