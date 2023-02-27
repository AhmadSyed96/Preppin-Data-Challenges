import pandas as pd
from pandasgui import show
import numpy as np
from datetime import datetime

with pd.ExcelFile('NBA 2018_19 Results.xlsx') as xl:
    df_games = pd.concat(pd.read_excel(xl, sheet).assign(Winner = lambda dfx : np.where(dfx['PTS'] > dfx['PTS.1'], dfx['Visitor/Neutral'], dfx['Home/Neutral']),
                                                         Date = lambda dfx : pd.to_datetime(dfx['Date'], errors='coerce'),
                                                         Game_Type = lambda dfx : np.where(dfx['Date'] <= datetime.strptime('2019-04-10', '%Y-%m-%d'), 'Regular Season', 'Plyoffs')) for sheet in xl.sheet_names)

df_games_per_team  = df_games.loc[df_games['Game_Type'] == 'Regular Season']\
                             .assign(Team = lambda dfx : dfx[['Visitor/Neutral', 'Home/Neutral']].apply(list, axis=1))\
                             .explode('Team')\
                             .assign(Win = lambda dfx : dfx['Winner'] == dfx['Team'],
                                     game = lambda dfx : dfx.groupby('Team')['Date'].rank(),
                                     Wins = lambda dfx : dfx.groupby('Team')['Win'].cumsum())\
                             .groupby(['Team', 'game'], as_index=False)['Wins'].min()\
                             .assign(rank = lambda dfx : dfx.groupby('game')['Wins'].rank(method='first'))
show(df_games_per_team)