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


# -*- coding: utf-8 -*-
"""
Preppin' Data 2020: Week 04
https://preppindata.blogspot.com/2020/01/2020-week-4.html
- Input data
- Change the Question Number for the question asked
- Clean the Country and Store names
  - We only want English names for places
- Clean up the dates and times to create a 'Completion Date' as a Date Time field
- Understand the age of the customer based on their Date of Birth (DoB)
  - Nulls are ok
  - Their age is taken to the date of 22nd January 2020
- Find the first answer for each customer in each store and country
- Find the latest answer for each customer in each store and country (if there
  are multiple responses)
- Remove any answers that are not a customer's first or latest
- Classify the 'NPS Recommendation' question based on the standard logic:
  - 0-6 makes the customer a 'Detractor'
  - 7-8 makes the customer a 'Passive'
  - 9-10 makes the customer a 'Promoter'
- Output the data
Author: Kelly Gilbert
Created: 2021-12-20
Requirements:
  - input datasets:
      - PD 2020 Wk 4 Input.csv
      - Store Survey Results - Question Sheet.csv
  - output dataset (for results check only):
      - PD 2020 Wk 4 Output
"""

# import datetime as dt
# from numpy import nan, where
# from pandas import pivot_table, read_csv, to_timedelta, to_datetime
#
#
# def age(begin, end):
#     """
#     calculates the number of full years between begin and end
#     """
#     return end.year - begin.year  # - ((end.month, end.day) < (begin.month, begin.day))
#
#
# def split_dict(in_dict):
#     """
#     add the list of misspelled names as keys, with the correct spelling as the value
#     """
#
#     new_dict = {i: k for k, v in in_dict.items() for i in v}
#     new_dict.update({k.lower(): k.title() for k in in_dict.keys()})
#     return new_dict
#
#
# CURRENT_DATE = dt.datetime(2020, 1, 22)
#
# # ---------------------------------------------------------------------------------------------------
# # input the data
# # ---------------------------------------------------------------------------------------------------
#
# df = read_csv('PD 2020 Wk 4 Input (1).csv', parse_dates=['DoB'], dayfirst=True)
# df_q = read_csv('Store Survey Results - Question Sheet (1).csv')
#
# # ---------------------------------------------------------------------------------------------------
# # process the data
# # ---------------------------------------------------------------------------------------------------
#
# # clean the Country and Store names
# # df['Country'].unique()
# # df['Store'].unique()
#
# country_dict = {'England': ['3ngland', 'egland', 'eggland', 'ingland'],
#                 'Scotland': ['sc0tland', 'scottish'],
#                 'United States': ['united state'],
#                 'Netherlands': ['the netherlands']}
#
# store_dict = {'Amsterdam': ['amstelveen']}
#
# df['Country'] = df['Country'].str.lower().replace(split_dict(country_dict)).str.title()
# df['Store'] = df['Store'].str.lower().replace(split_dict(store_dict)).str.title()
#
# # summarize response attributes by Response #
# # pivot_table excludes records if any of these cols are null, such as the DoB
# df_r = df.drop_duplicates(subset='Response')[[c for c in df.columns if c not in ['Question Number', 'Answer']]]
#
# # pivot questions by Response # and merge back to the attributes
# df_p = df.pivot_table(index=['Response'], values='Answer', columns='Question Number', aggfunc='first') \
#     .reset_index() \
#     .merge(df_r, how='inner', on='Response')
#
# # rename the columns
# #     I chose to pivot using the numeric column names vs. merging the question list, because it would
# #     save memory for a large dataset vs. repeating the question for every row.
# question_dict = {n: q for n, q in zip(df_q['Number'], df_q['Question'])}
# df_p.columns = [question_dict.get(c, c) for c in df_p.columns]
#
# # clean date and time, create Completion Date column
# df_p['Date'] = to_datetime(df_p['What day did you fill the survey in?'],
#                            dayfirst=True, errors='coerce')
#
# df_p['Date'] = where(df_p['Date'].isna(),
#                      to_datetime(df_p['What day did you fill the survey in?']
#                                  .str.replace('.* - (.*)', '\\1 ' + str(CURRENT_DATE.year), regex=True)),
#                      df_p['Date'])
#
# df_p[['Hour', 'Minute', 'AMPM']] = df_p['What time did you fill the survey in?'] \
#     .str.replace('.', ':', regex=False) \
#     .str.extract('(\d{1,2}):?(\d{2})\s?(.*)')
#
# df_p['Hour'] = df_p['Hour'].astype(int) + where(df_p['AMPM'].str.lower().str.contains('pm'), 12, 0)
# df_p['Minute'] = df_p['Minute'].astype(int)
#
# df_p['Completion Date'] = df_p['Date'] \
#                           + to_timedelta(df_p['Hour'], unit='h') \
#                           + to_timedelta(df_p['Minute'], unit='m')
#
# # understand the age of the customer based on their Date of Birth (DoB)
# df_p['Age of Customer'] = df_p['DoB'].apply(lambda x: age(x, CURRENT_DATE))
#
# # remove any answers that are not a customer's first or latest
# group_cols = ['Name', 'Store', 'Country']
# df_p['Result'] = where(df_p['Completion Date'] == df_p.groupby(group_cols)['Completion Date'].transform('min'),
#                        'First',
#                        where(df_p['Completion Date'] == df_p.groupby(group_cols)['Completion Date'].transform('max'),
#                              'Latest', 'Other'))
# print(df_p)
# df_p = df_p.loc[df_p['Result'] != 'Other']
#
# # classify NPS recommendation
# score_field = 'Would you recommend C&BSco to your friends and family? (Score 0-10)'
# df_p['Detractor'] = where(df_p[score_field].astype(int) <= 6, 1, nan)
# df_p['Passive'] = where((df_p[score_field].astype(int) >= 7)
#                         & (df_p[score_field].astype(int) <= 8), 1, nan)
# df_p['Promoter'] = where(df_p[score_field].astype(int) > 8, 1, nan)