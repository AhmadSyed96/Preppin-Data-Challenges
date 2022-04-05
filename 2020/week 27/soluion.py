import pandas as pd
import numpy as np
from pandasgui import show

df_surfer = pd.read_excel('Input (1).xlsx', sheet_name='Preppers')\
              .assign(Surfer_ID = lambda dfx : np.arange(len(dfx)) + 1,
                      Season = lambda dfx : dfx['Season'].str.split(', '),
                      Board_Type = lambda dfx : dfx['Board Type'].str.split(', '),
                      Skill = lambda dfx : dfx['Skill'].str.strip())\
              .drop(columns=['Board Type'])\
              .explode('Season')\
              .explode('Board_Type')

df_location = pd.read_excel('Input (1).xlsx', sheet_name='Location')\
                .assign(Site = lambda dfx : dfx['Site'].str.extract('(.*)\s-\s.*'))

df_info = pd.read_excel('Input (1).xlsx', sheet_name='Information', header=1, skipfooter=2)\
            .assign(Surf_Site = lambda dfx : dfx['Surf Site'].str.strip(),
                    Beach_ID = lambda dfx : np.arange(len(dfx)) + 1)\
            .drop(columns=['Surf Site'])\
            .merge(df_location, how='left', left_on='Surf_Site', right_on='Site')\
            .assign(Boards = lambda dfx : dfx['Boards'].str.split(', '),
                    Skill_Level = lambda dfx : dfx['Skill Level'].str.split(', '),
                    Surf_Season = lambda dfx : dfx['Surf Season'].str.split(', '))\
            .drop(columns=['Skill Level', 'Surf Season'])\
            .explode('Boards').explode('Skill_Level').explode('Surf_Season')

# show(df_surfer, df_info)
df_output =   pd.merge(df_surfer, df_info,
                     left_on=['Skill', 'Season', 'Board_Type'],
                     right_on=['Skill_Level', 'Surf_Season', 'Boards'])\
                .drop_duplicates(subset=['Beach_ID', 'Surfer_ID'])\
                .assign(Reliability_Rank = lambda dfx : dfx['Reliability'].map({'Rarely Breaks' : 5,
                                                                                'Inconsistent' : 4,
                                                                                'Fairly Inconsistent' : 3,
                                                                                'Fairly Consistent' : 2,
                                                                                'Very Consistent' : 1}),
                        Beach_Rank = lambda dfx : dfx.sort_values(by=['Rating', 'Reliability_Rank'], ascending=(False, True)).groupby('Name')['Site'].transform('cumcount'),
                        Surfer_Minimum = lambda dfx : dfx.groupby('Name')['Beach_Rank'].transform('min'))\
                .query('Beach_Rank == Surfer_Minimum')
show(df_info, df_surfer, df_output)
