import pandas as pd
from pandasgui import show
import numpy as np

df_polls = pd.read_csv('PD 2020 Wk 9 Input - Sheet1.csv').drop(0).assign(Start_Date=lambda df_x:df_x['Date'].str.extract('(\d+/\d+)\s'),
                                                                   End_Date=lambda df_x:df_x['Date'].str.extract('.*\s(\d+/\d+)'),
                                                                   Sample_Type=lambda df_x:df_x['Sample'].str[-2:])\
                                                    .replace({'RV':'Registered Voter', 'LV':'Likely Voter'})
# show(df_polls)

df_candidates = df_polls.melt(id_vars=['Poll', 'Date', 'Sample', 'Start_Date', 'End_Date', 'Sample_Type'], var_name='Candidate', value_name='Poll Results')
df_candidates = df_candidates[df_candidates['Poll Results'] != '--'].reset_index(drop=True)
df_candidates['Poll Results'] = df_candidates['Poll Results'].astype('int')
df_candidates['Poll Rank'] = df_candidates.groupby(['Poll','End_Date'])['Poll Results'].rank(method='max', ascending=False)
df_candidates['1st'] = df_candidates.groupby(['Poll', 'End_Date'])['Poll Results'].transform('max')
df_candidates['2nd'] = df_candidates.groupby(['Poll', 'End_Date'])['Poll Results'].transform(lambda x: x.nlargest(2).min())
df_candidates['Diff'] = df_candidates['1st'] - df_candidates['2nd']
show(df_candidates)
