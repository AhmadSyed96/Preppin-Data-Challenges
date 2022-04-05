import pandas as pd
import numpy as np
from pandasgui import show

def get_GOoP(dfx):
    dfx1 = dfx[dfx['position_type'] != dfx['position preferred']]
    dfx2 = dfx1.groupby('player name', as_index=False)['appeared'].sum().rename(columns={'appeared':'Games Out of Position'})
    dfx3 = pd.merge(dfx2, dfx,how='right', on='player name')
    return dfx3['Games Out of Position']

def get_minutes(dfx):
    # melt to get sub in column
    dfx1 = dfx.melt(id_vars=['No.', 'position number', 'Position Name', 'position_abbr', 'started_as'],
                            value_vars=['first player subbing in', 'second player subbing in',
                                        'third player subbing in'],
                            value_name='sub in',
                            var_name='sub in type') \
        .drop(columns=['sub in type'])
    dfx1 = dfx1.set_index(
        ['No.', 'position number', 'Position Name', 'position_abbr', 'started_as',
         dfx1.groupby(['No.', 'position number', 'Position Name', 'position_abbr', 'started_as']).cumcount()])

    # melt to get sub out col
    dfx2 = dfx.melt(id_vars=['No.', 'position number', 'Position Name', 'position_abbr', 'started_as'],
                            value_vars=['first player subbing out', 'second player subbing out',
                                        'third player subbing out'],
                            value_name='sub out',
                            var_name='sub out type') \
        .drop(columns=['sub out type'])
    dfx2 = dfx2.set_index(
        ['No.', 'position number', 'Position Name', 'position_abbr', 'started_as',
         dfx1.groupby(['No.', 'position number', 'Position Name', 'position_abbr', 'started_as']).cumcount()])
    # melt to get sub time col
    dfx3 = dfx.melt(id_vars=['No.', 'position number', 'Position Name', 'position_abbr', 'started_as'],
                            value_vars=['first sub time', 'second sub time', 'third sub time'],
                            value_name='sub time',
                            var_name='sub time type') \
        .drop(columns=['sub time type'])
    dfx3 = dfx3.set_index(
        ['No.', 'position number', 'Position Name', 'position_abbr', 'started_as',
         dfx1.groupby(['No.', 'position number', 'Position Name', 'position_abbr', 'started_as']).cumcount()])
    # concat the results
    dfx4 = (pd.concat([dfx1, dfx2, dfx3], axis=1)
            .sort_index(level=5)
            .reset_index(level=5, drop=True)
            .reset_index())
    # show(dfx4)

    # merge dfx to get sub out pos name. then get act pos & act pos abr
    dfx5 = pd.merge(dfx4, dfx[['No.', 'position number', 'position_abbr']].add_suffix('_right'),
                    how='left',
                    left_on=['No.', 'sub out'], right_on=['No._right', 'position number_right']) \
        .drop(columns=['No._right', 'position number_right']) \
        .rename(columns={'position_abbr_right': 'sub out position abbr'})
    dfx6 = pd.merge(dfx5, dfx[['No.', 'position number', 'Position Name']].add_suffix('_right'),
                    how='left',
                    left_on=['No.', 'sub out'], right_on=['No._right', 'position number_right']) \
        .drop(columns=['No._right', 'position number_right']) \
        .rename(columns={'Position Name_right': 'sub out position name'})
    dfx6['played as'] = np.where(dfx6['started_as'] == 'sub', dfx6['sub out position name'], dfx6['Position Name'])
    dfx6['position type'] = np.where(dfx6['started_as'] == 'sub', dfx6['sub out position abbr'], dfx6['position_abbr'])

    # then seperate by starting as col as to get the mins columns correct. union after
    dfx6['mins'] = np.where(dfx4['started_as'] == 'starter',
                            np.where(dfx4['position number'] == dfx4['sub out'],
                                     dfx4['sub time'],
                                     90),
                            np.where(dfx4['position number'] == dfx4['sub in'],
                                     90 - dfx4['sub time'],
                                     np.nan))

    dfx7_sub = dfx6[dfx6['started_as'] == 'sub']
    dfx7_starter = dfx6[dfx6['started_as'] == 'starter']
    #
    dfx8_1 = dfx7_sub.groupby(['No.', 'position number', 'played as', 'position type'], as_index=False)['mins'].max()
    dfx8_2 = dfx7_starter.groupby(['No.', 'position number', 'played as', 'position type'], as_index=False)['mins'].min()

    dfx9 = pd.concat([dfx8_1, dfx8_2]).dropna(subset=['mins'])
    dfx10 = pd.merge(dfx9, dfx, on=['No.', 'position number'], how='right')
    return dfx10



df_player = pd.read_excel('PlayerList (1).xlsx')\
                .assign(jersey_number = lambda dfx : dfx['Player Name'].str.extract('(\d{1,2})'),
                        position_preferred = lambda dfx : dfx['Player Name'].str.extract('\((.)\)'),
                        full_name = lambda dfx : dfx['Player Name'].str.extract('\d+(.*)\s\(.\)'),
                        space = lambda dfx : dfx['full_name'].str.contains('\s'),
                        incomplete_extract = lambda dfx : dfx['full_name'].str.extract('\w\s(.*)'),
                        last_name = lambda dfx : np.where(dfx['space'], dfx['incomplete_extract'], dfx['full_name']))\
                .rename(columns=lambda x: x.replace('_', ' '))\
                .drop(columns=['Player Name', 'full name', 'space', 'incomplete extract'])

df_formations = pd.read_excel('Formation Positions (1).xlsx')\
                    .assign(position_abbr = lambda dfx : dfx['Position Type'].str[0])

df_lineups = pd.read_excel('Liverpool Lineups (1).xlsx',skiprows=5, header=1)\
                .dropna(axis=1, how='all')\
                .rename(columns={'sub1' : 'first player subbing out', 'Unnamed: 22' : 'first player subbing in', 'Unnamed: 23' : 'first sub time',
                                 'sub2' : 'second player subbing out', 'Unnamed: 25' : 'second player subbing in', 'Unnamed: 26' : 'second sub time',
                                 'sub3' : 'third player subbing out', 'Unnamed: 28' : 'third player subbing in', 'Unnamed: 29' : 'third sub time',
                                 1:'1', 2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9', 10:'10', 11:'11', 12:'12', 13:'13', 14:'14', 15:'15', 16:'16', 17:'17', 18:'18'})\



df_output_2 = df_lineups.melt(id_vars=['No.', 'Date', 'Comp.', 'Formation', 'first player subbing in', 'first player subbing out', 'first sub time',
                                           'second player subbing in', 'second player subbing out', 'second sub time',
                                           'third player subbing in', 'third player subbing out', 'third sub time'],
                                  value_vars=['1', '2', '3', '4', '5', '6',
                                              '7', '8', '9', '10', '11',
                                              '12', '13', '14', '15', '16', '17', '18'],
                                  value_name='player name',
                                  var_name='position number')\
                        .astype({'position number' : 'int64'})\
                        .merge(df_formations, left_on=['Formation','position number'], right_on=['Formation Name','Player Position'])\
                        .drop(columns=['Formation Name', 'Player Position', 'Position Type'])\
                        .assign(started_as=lambda dfx: np.where(dfx['position number'].between(1,11), 'starter', 'sub'),
                                minutes=lambda dfx: get_minutes(dfx)['mins'],
                                played_as = lambda dfx: get_minutes(dfx)['played as'],
                                position_type = lambda dfx : get_minutes(dfx)['position type'],
                                appeared = lambda dfx : np.where((dfx['minutes'] < 1) | (dfx['minutes'].isna()), 0, 1))\
                        .drop(columns=['Position Name', 'position_abbr'])\
                        .groupby(['player name', 'position_type', 'played_as'], as_index=False).agg({'minutes' : 'sum', 'appeared' : 'sum'}) \
                        .merge(df_player, left_on='player name', right_on='last name') \
                        .assign(GOoP=lambda dfx: get_GOoP(dfx))


df_output_1 = df_lineups.assign(left_Goals = lambda dfx : dfx['Result'].str.extract('(.*)\-.*').astype('int'),
                                right_Goals = lambda dfx : dfx['Result'].str.extract('.*\-(.*)').astype('int'),
                                Home_Goals = lambda dfx : np.where(dfx['Location']=='H', dfx['left_Goals'], dfx['right_Goals']),
                                Away_Goals = lambda dfx : np.where(dfx['Location']=='H', dfx['right_Goals'], dfx['left_Goals']))\
                        .groupby(['Formation', 'Oppo Form.'], as_index=False).agg({'No.':'count', 'Home_Goals':'sum', 'Away_Goals':'sum'})
show(df_lineups ,df_output_1)

