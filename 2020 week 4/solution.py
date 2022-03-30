import pandas as pd
import numpy as np
from pandasgui import show
import datetime as dt



def split_dict(in_dict):

    ##make a list for the replace function {wong word : right word, wong word2 : right word2}
    new_dict = {}
    for right_word,wrong_word_list in in_dict.items():
        for wrong_word in wrong_word_list:
            new_dict[wrong_word] = right_word
    return new_dict


df = pd.read_csv('PD 2020 Wk 4 Input (1).csv')
# print(df)

pdf = df.pivot(index= 'Response', columns='Question Number', values='Answer').reset_index()
# print(pdf.columns)

df_q = pd.read_csv('Store Survey Results - Question Sheet (1).csv')
question_dict = {n : q for n, q in zip(df_q['Number'], df_q['Question'])}
pdf.columns = [question_dict.get(c,c) for c in pdf.columns]
# print(pdf)

country_dict = { 'England' : ['3ngland', 'egland', 'eggland', 'ingland'],
                 'Scotland' : ['sc0tland', 'scottish'],
                 'United States' : ['united state'],
                 'Netherlands' : ['the netherlands'] }

store_dict = { 'Amsterdam' : ['amstelveen']}
print(df.Country.unique())
df['Country'] = df['Country'].str.lower().replace(split_dict(country_dict)).str.title()
df['Store'] = df['Store'].str.lower().replace(split_dict(store_dict)).str.title()
unq_df = df.drop_duplicates(subset='Response')[[c for c in df.columns if c not in ['Question Number', 'Answer']]]
new_df = pdf.merge(unq_df,on='Response')
# show(new_df)

current_date = dt.datetime(2020, 1, 22)
new_df['Date'] = pd.to_datetime(new_df['What day did you fill the survey in?'],
                           dayfirst=True, errors='coerce')
new_df['Date'] = np.where(new_df['Date'].isna(), pd.to_datetime(new_df['What day did you fill the survey in?'].str.replace('.*-(.*)', '\\1 '+str(current_date.year),regex=True)), new_df['Date'])
new_df[['Hour', 'Minute', 'AMPM']] = new_df['What time did you fill the survey in?'].str.replace('.',':', regex=False).str.extract('(\d{1,2}):?(\d{1,2})\s?(.*)')
new_df['Hour'] = new_df['Hour'].astype('int') + np.where(new_df['AMPM'].str.lower().str.contains('pm'),12,0)
new_df['Minute'] = new_df['Minute'].astype('int')
new_df['Completion Date'] = new_df['Date'] + pd.to_timedelta(new_df['Hour'], unit='h') + pd.to_timedelta(new_df['Minute'], unit='m')
# show(new_df)


group_cols = ['Name', 'Store', 'Country']
new_df['result'] = np.where(new_df['Completion Date'] == new_df.groupby(group_cols)['Completion Date'].transform('min'), 'First'
                            , np.where(new_df['Completion Date'] == new_df.groupby(group_cols)['Completion Date'].transform('max'), 'Latest', 'Other'))
new_df = new_df[new_df['result'] != 'Other']
# print(new_df)


score_field = 'Would you recommend C&BSco to your friends and family? (Score 0-10)'
new_df['Detractor'] = np.where(new_df[score_field].astype('int')<=6,1,np.nan)
new_df['Passive'] = np.where((new_df[score_field].astype('int')>=7)&(new_df[score_field].astype('int')<=8),1,np.nan)
new_df['Promoter'] = np.where(new_df[score_field].astype('int') > 8, 1, np.nan)
# print(new_df)
