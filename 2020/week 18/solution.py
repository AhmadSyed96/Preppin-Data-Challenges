import pandas as pd
import numpy as np
from pandasgui import show

def get_minutes(dfx):
    dfx1 = dfx.melt(id_vars=['No.', 'player_number', 'started_as'],
                  value_vars=['first player subbing in', 'second player subbing in', 'third player subbing in'],
                  value_name='sub in',
                  var_name='sub in type') \
        .drop(columns=['sub in type'])
    dfx1 = dfx1.set_index(
        ['No.', 'player_number', 'started_as', dfx1.groupby(['No.', 'player_number', 'started_as']).cumcount()])
    dfx2 = dfx.melt(id_vars=['No.', 'player_number', 'started_as'],
                  value_vars=['first player subbing out', 'second player subbing out', 'third player subbing out'],
                  value_name='sub out',
                  var_name='sub out type') \
        .drop(columns=['sub out type'])
    dfx2 = dfx2.set_index(
        ['No.', 'player_number', 'started_as', dfx1.groupby(['No.', 'player_number', 'started_as']).cumcount()])
    dfx3 = dfx.melt(id_vars=['No.', 'player_number', 'started_as'],
                  value_vars=['first sub time', 'second sub time', 'third sub time'],
                  value_name='sub time',
                  var_name='sub time type') \
        .drop(columns=['sub time type'])
    dfx3 = dfx3.set_index(
        ['No.', 'player_number', 'started_as', dfx1.groupby(['No.', 'player_number', 'started_as']).cumcount()])
    dfx4 = (pd.concat([dfx1, dfx2, dfx3], axis=1)
           .sort_index(level=3)
           .reset_index(level=3, drop=True)
           .reset_index())
    dfx4['mins'] = np.where(dfx4['started_as'] == 'starter',
                           np.where(dfx4['player_number'] == dfx4['sub out'],
                                    dfx4['sub time'],
                                    90),
                           np.where(dfx4['player_number'] == dfx4['sub in'],
                                    90 - dfx4['sub time'],
                                    np.nan))
    dfx5 = dfx4.groupby(['No.', 'player_number'])['mins'].min()
    dfx6 = pd.merge(dfx, dfx5, on=['No.', 'player_number'])
    return dfx6['mins']

df = pd.read_excel('Liverpool Lineups (1).xlsx',skiprows=5, header=1)\
        .dropna(axis=1, how='all')\
        .rename(columns={'sub1' : 'first player subbing out', 'Unnamed: 22' : 'first player subbing in', 'Unnamed: 23' : 'first sub time',
                         'sub2' : 'second player subbing out', 'Unnamed: 25' : 'second player subbing in', 'Unnamed: 26' : 'second sub time',
                         'sub3' : 'third player subbing out', 'Unnamed: 28' : 'third player subbing in', 'Unnamed: 29' : 'third sub time',
                         1 : 'starter 1', 2 : 'starter 2', 3 : 'starter 3', 4 : 'starter 4', 5 : 'starter 5',
                         6 : 'starter 6', 7 : 'starter 7', 8 : 'starter 8', 9 : 'starter 9', 10 : 'starter 10',11 : 'starter 11',
                         12 : 'sub 12', 13 : 'sub 13', 14 : 'sub 14', 15 : 'sub 15', 16 : 'sub 16', 17 : 'sub 17', 18 : 'sub 18'})\
        .astype({'third player subbing in' : 'int64', 'third player subbing out' : 'int64', 'third sub time' : 'int64'}, errors='ignore')\
        .melt(id_vars=['No.', 'Date', 'Comp.', 'first player subbing in', 'first player subbing out', 'first sub time',
                       'second player subbing in', 'second player subbing out', 'second sub time',
                       'third player subbing in', 'third player subbing out', 'third sub time'],
              value_vars=['starter 1', 'starter 2', 'starter 3', 'starter 4', 'starter 5', 'starter 6',
                          'starter 7', 'starter 8', 'starter 9', 'starter 10', 'starter 11',
                          'sub 12', 'sub 13', 'sub 14', 'sub 15', 'sub 16', 'sub 17', 'sub 18'],
              value_name='player')\
        .assign(player_number = lambda dfx : dfx.variable.str.split(' ', expand=True)[1].astype('float64'),
                started_as = lambda dfx : dfx.variable.str.split(' ', expand=True)[0],
                minutes = lambda dfx : get_minutes(dfx),
                appeared = lambda dfx : np.where((dfx['minutes'] < 1) | (dfx['minutes'].isna()), 0, 1))\
        .groupby('player').agg({'No.' :  'count',
                                'appeared' : 'sum',
                                'minutes' : 'sum'})\
        .rename(columns = {'No.' :  'In Squad',
                           'appeared' : 'appearances',
                           'minutes' : 'total minutes played'})\
        .assign(Mins_Per_Game = lambda dfx : dfx['total minutes played'] / dfx['appearances'])
