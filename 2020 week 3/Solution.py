import pandas as pd
import numpy as np
from pandasgui import show
from datetime import datetime as dt

Excelfile = pd.ExcelFile('PD - NBA Results (1).xlsx')

Teams = pd.read_excel(Excelfile, sheet_name='Team List')
# print(Teams)

sheet_to_df_map = {}
for sheet_name in Excelfile.sheet_names:
    if 'Results' in sheet_name:
        sheet_to_df_map[sheet_name] = Excelfile.parse(sheet_name)
results = pd.concat(sheet_to_df_map,ignore_index=True)
# print(results.columns.values)
results = results.drop(['Unnamed: 6', 'Unnamed: 7', 'Attend.', 'Notes', 'Start (ET)'], axis=1)
results = results.rename(columns={'PTS.1': 'Home Points', 'Visitor/Neutral': 'Visiting Team', 'PTS': 'Visiting Points', 'Home/Neutral': 'Home Team'})
results = results[results['Home Points'].notna()]
# print(results)

results['Winner'] = np.where(results['Visiting Points'] > results['Home Points'], results['Visiting Team'], results['Home Team'])
results['Loser'] = np.where(results['Visiting Points'] > results['Home Points'], results['Home Team'], results['Visiting Team'])
# print(results.head(1))

results = results.merge(Teams, left_on='Winner', right_on='Team').drop(columns=['Team','Divison']).rename(columns={'Conference':'Winner Conference'})
results = results.merge(Teams, left_on='Loser', right_on='Team').drop(columns=['Team','Divison']).rename(columns={'Conference':'Loser Conference'})
results['In Conf?'] = np.where(results['Winner Conference'] == results['Loser Conference'],1,0)
show(results)
id_vars = ['Date', 'Home Team', 'Visiting Team',
           'Loser Conference', 'Winner Conference', 'In Conf?']
results = pd.melt(results, id_vars=id_vars,  value_vars=['Winner', 'Loser'],
          var_name='team_type', value_name='Team')
results['conference'] = np.where(results['team_type']=='Winner', results['Winner Conference'], results['Loser Conference'])
results.drop(columns=['Loser Conference', 'Winner Conference'], inplace=True)
show(results)

# flags for summarization
results['home_flag'] = np.where(results['Team']==results['Home Team'], 1, 0)
results['away_flag'] = np.where(results['Team']==results['Visiting Team'], 1, 0)

results['win_flag'] = np.where(results['team_type']=='Winner', 1, np.nan)
results['loss_flag'] = np.where(results['team_type']=='Loser', 1, np.nan)

results['Date'] = pd.to_datetime(results['Date'], infer_datetime_format=True)
results.sort_values(['Team', 'Date'], ascending=False, inplace=True)
results['win_streak'] = results.groupby('Team')['win_flag'].cumsum(skipna=False) # this will count up from one until it hits a NaN
results['loss_streak'] = results.groupby('Team')['loss_flag'].cumsum(skipna=False)


results['win_flag'] = results['win_flag'].fillna(0)
results['loss_flag'] = results['loss_flag'].fillna(0)

results['conference_win_flag'] = np.where((results['team_type']=='Winner') & (results['In Conf?']==1), 1, 0)
results['conference_loss_flag'] = np.where((results['team_type']=='Loser') & (results['In Conf?']==1), 1, 0)

results['home_win_flag'] = np.where((results['team_type']=='Winner') & (results['home_flag']==1), 1, 0)
results['home_loss_flag'] = np.where((results['team_type']=='Loser') & (results['home_flag']==1), 1, 0)

results['away_win_flag'] = np.where((results['team_type']=='Winner') & (results['away_flag']==1), 1, 0)
results['away_loss_flag'] = np.where((results['team_type']=='Loser') & (results['away_flag']==1), 1, 0)

results['date_rank'] = results.groupby('Team')['Date'].rank(method='first', ascending=False)
results['L10_win_flag'] = np.where((results['team_type']=='Winner') & (results['date_rank']<=10), 1, 0)
results['L10_loss_flag'] = np.where((results['team_type']=='Loser') & (results['date_rank']<=10), 1, 0)
show(results)

results_summary = results.groupby(['conference','Team'], as_index=False).agg(
               { 'win_flag' : 'sum',
                 'loss_flag' : 'sum',
                 'conference_win_flag' : 'sum',
                 'conference_loss_flag' : 'sum',
                 'home_win_flag' : 'sum',
                 'home_loss_flag' : 'sum',
                 'away_win_flag' : 'sum',
                 'away_loss_flag' : 'sum',
                 'L10_win_flag' : 'sum',
                 'L10_loss_flag' : 'sum',
                 'win_streak' : 'max',
                 'loss_streak' :  'max'
               }
             ).rename(columns=
               { 'win_flag' : 'W',
                 'loss_flag' : 'L',
                 'conference_win_flag' : 'Conf_W',
                 'conference_loss_flag' : 'Conf_L' ,
                 'home_win_flag' : 'Home_W' ,
                 'home_loss_flag' : 'Home_L' ,
                 'away_win_flag' : 'Away_W' ,
                 'away_loss_flag' : 'Away_L',
                 'L10_win_flag' : 'L10_W' ,
                 'L10_loss_flag' : 'L10_L' ,
                 'win_streak' : 'Strk_W' ,
                 'loss_streak' : 'Strk_L'
               }
             )
show(results_summary)


# remove the extra column index level and convert numbers to integer
# results_summary.columns = [c[0] if c[1]=='' else c[1] for c in results_summary.columns]
results_summary['Strk_W'] = results_summary['Strk_W'].fillna(0)
results_summary['Strk_L'] = results_summary['Strk_L'].fillna(0)
# print(results_summary)


results_summary['Pct'] = (results_summary['W'] / (results_summary['W'] + results_summary['L'])).round(3)
results_summary['Conf'] = results_summary['Conf_W'].astype(str) + '-' + results_summary['Conf_L'].astype(str)
results_summary['Home'] = results_summary['Home_W'].astype(str) + '-' + results_summary['Home_L'].astype(str)
results_summary['Away'] = results_summary['Away_W'].astype(str) + '-' + results_summary['Away_L'].astype(str)
results_summary['L10'] = results_summary['L10_W'].astype(str) + '-' + results_summary['L10_L'].astype(str)
results_summary['Strk'] = np.where(results_summary['Strk_W']==0, 'L' + results_summary['Strk_L'].astype(str),
                                                    'W' + results_summary['Strk_W'].astype(str))
show(results_summary)



# conference rank
results_summary['Rank'] = results_summary.groupby('conference')['Pct'].rank(method='max', ascending=False)
results_summary.sort_values(['conference', 'Rank'], ascending=True, inplace=True)

show(results_summary)











#
# from datetime import datetime as dt
# from numpy import where, nan, set_printoptions
# from os import chdir
# from pandas import concat, ExcelFile, ExcelWriter, melt, set_option
# desired_width=320
# set_option('display.width', desired_width)
# set_printoptions(linewidth=desired_width)
# set_option('display.max_columns',20)
# set_option('display.max_rows',200)
#
# # import the data
# # chdir('C:\Users\ahmad\Downloads\dataprep python solutions\2020 week 3\PD - NBA Results (1).xlsx')
# xl = ExcelFile(r'PD - NBA Results (1).xlsx')
#
#
# # import the team info and correct spelling of Division
# df_team = xl.parse('Team List')
# df_team.rename(columns = {'Divison':'Division'}, inplace = True)
#
#
# # concatenate the results sheets
# result_sheets = [s for s in xl.sheet_names if 'Results' in s]
# df = None
# for sheet in result_sheets:
#     df = concat([df, xl.parse(sheet)])
#
#
# # keep necessary columns, remove future games, identify winner/loser
# df = df[['Date', 'Visitor/Neutral', 'PTS', 'Home/Neutral', 'PTS.1']]
# df = df[df['PTS'].notna()]
# print(df)
# df['winner'] = where(df['PTS']>=df['PTS.1'], df['Visitor/Neutral'], df['Home/Neutral'])
# df['loser'] = where(df['PTS']>=df['PTS.1'], df['Home/Neutral'], df['Visitor/Neutral'])
#
#
# # convert date
# df['Date'] = [dt.strptime(d, '%a %b %d %Y') for d in df['Date']]
#
#
# # add the conferences
# df = df.merge(df_team, left_on='winner', right_on='Team', how='left') \
#      .drop(columns=['Team','Division'])
# df = df.merge(df_team, left_on='loser', right_on='Team', how='left',
#               suffixes=('_winner', '_loser')).drop(columns=['Team','Division'])
# df['in_conference'] = where(df['Conference_winner']==df['Conference_loser'], 1, 0)
#
#
# # put winner/loser into separate rows
# id_vars = ['Date', 'Home/Neutral', 'Visitor/Neutral',
#            'Conference_winner', 'Conference_loser', 'in_conference']
# df = melt(df, id_vars=id_vars,  value_vars=['winner', 'loser'],
#           var_name='team_type', value_name='Team')
# df['conference'] = where(df['team_type']=='winner', df['Conference_winner'], df['Conference_loser'])
# df.drop(columns=['Conference_winner', 'Conference_loser'], inplace=True)
#
#
# # flags for summarization
# df['home_flag'] = where(df['Team']==df['Home/Neutral'], 1, 0)
# df['away_flag'] = where(df['Team']==df['Visitor/Neutral'], 1, 0)
#
# df['win_flag'] = where(df['team_type']=='winner', 1, nan)
# df['loss_flag'] = where(df['team_type']=='loser', 1, nan)
#
# df.sort_values(['Team', 'Date'], ascending=False, inplace=True)
# df['win_streak'] = df.groupby('Team')['win_flag'].cumsum(skipna=False) # this will count up from one until it hits a NaN
# df['loss_streak'] = df.groupby('Team')['loss_flag'].cumsum(skipna=False)
#
# df['win_flag'] = df['win_flag'].fillna(0)
# df['loss_flag'] = df['loss_flag'].fillna(0)
#
# df['conference_win_flag'] = where((df['team_type']=='winner') & (df['in_conference']==1), 1, 0)
# df['conference_loss_flag'] = where((df['team_type']=='loser') & (df['in_conference']==1), 1, 0)
#
# df['home_win_flag'] = where((df['team_type']=='winner') & (df['home_flag']==1), 1, 0)
# df['home_loss_flag'] = where((df['team_type']=='loser') & (df['home_flag']==1), 1, 0)
#
# df['away_win_flag'] = where((df['team_type']=='winner') & (df['away_flag']==1), 1, 0)
# df['away_loss_flag'] = where((df['team_type']=='loser') & (df['away_flag']==1), 1, 0)
#
# df['date_rank'] = df.groupby('Team')['Date'].rank(method='first', ascending=False)
# df['L10_win_flag'] = where((df['team_type']=='winner') & (df['date_rank']<=10), 1, 0)
# df['L10_loss_flag'] = where((df['team_type']=='loser') & (df['date_rank']<=10), 1, 0)
#
#
# # summarize by team
# df_summary = df.groupby(['conference','Team'], as_index=False).agg(
#                { 'win_flag' : 'sum',
#                  'loss_flag' : 'sum',
#                  'conference_win_flag' : 'sum',
#                  'conference_loss_flag' : 'sum',
#                  'home_win_flag' : 'sum',
#                  'home_loss_flag' : 'sum',
#                  'away_win_flag' : 'sum',
#                  'away_loss_flag' : 'sum',
#                  'L10_win_flag' : 'sum',
#                  'L10_loss_flag' : 'sum',
#                  'win_streak' : 'max',
#                  'loss_streak' :  'max'
#                }
#              ).rename(
#                { 'win_flag' : 'W',
#                  'loss_flag' : 'L',
#                  'conference_win_flag' : 'Conf_W',
#                  'conference_loss_flag' : 'Conf_L' ,
#                  'home_win_flag' : 'Home_W' ,
#                  'home_loss_flag' : 'Home_L' ,
#                  'away_win_flag' : 'Away_W' ,
#                  'away_loss_flag' : 'Away_L',
#                  'L10_win_flag' : 'L10_W' ,
#                  'L10_loss_flag' : 'L10_L' ,
#                  'win_streak' : 'Strk_W' ,
#                  'loss_streak' : 'Strk_L'
#                }
#              )
#
# # print(df_summary.head(20))
# # # remove the extra column index level and convert numbers to integer
# # df_summary.columns = [c[0] if c[1]=='' else c[1] for c in df_summary.columns]
# # df_summary = concat([df_summary[['conference','Team']], df_summary.iloc[:, 2:].fillna(0).astype(int)], axis=1)
# #
# #
# # # calculations
# # df_summary['Pct'] = (df_summary['W'] / (df_summary['W'] + df_summary['L'])).round(3)
# # df_summary['Conf'] = df_summary['Conf_W'].astype(str) + '-' + df_summary['Conf_L'].astype(str)
# # df_summary['Home'] = df_summary['Home_W'].astype(str) + '-' + df_summary['Home_L'].astype(str)
# # df_summary['Away'] = df_summary['Away_W'].astype(str) + '-' + df_summary['Away_L'].astype(str)
# # df_summary['L10'] = df_summary['L10_W'].astype(str) + '-' + df_summary['L10_L'].astype(str)
# # df_summary['Strk'] = where(df_summary['Strk_W']==0, 'L' + df_summary['Strk_L'].astype(str),
# #                                                     'W' + df_summary['Strk_W'].astype(str))
# #
# # # conference rank
# # df_summary['Rank'] = df_summary.groupby('conference')['Pct'].rank(method='max', ascending=False)
# # df_summary.sort_values(['conference', 'Rank'], ascending=True, inplace=True)
# #     # the provided output isn't sorted
# #
# # # output one sheet per conference
# # cols = ['Rank', 'Team', 'W', 'L', 'Pct', 'Conf', 'Home', 'Away', 'L10', 'Strk']
# # writer = ExcelWriter(r'.\outputs\output-2020-03.xlsx', engine='xlsxwriter')
# #
# # for c in df_summary['conference'].unique():
# #     df_summary[df_summary['conference']==c].to_excel(writer, columns=cols,
# #                                                      sheet_name=c + 'ConferenceStandings',
# #                                                      index = False)