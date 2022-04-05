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










