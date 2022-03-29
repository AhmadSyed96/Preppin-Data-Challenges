import pandas as pd
import numpy as np
from pandasgui import show
from fuzzywuzzy import process, fuzz

df_survey = pd.read_excel('PD 2020W17 Survey (1).xlsx')\
                .drop_duplicates(subset=['What is your name?'])\
                .rename(columns={'What is your name?' : 'name',
                                 'How have you been watching Netflix? (Phone, TV, etc.)' : 'device used',
                                 'What have you been binging during lockdown?' : 'shows watched',
                                 'How would you rate Tiger King?' : 'Tiger King',
                                 'How would you rate Community?': 'Community',
                                 'How would you rate Brooklyn Nine-Nine?' : 'Brooklyn Nine-Nine',
                                 'How would you rate Love is Blind?' : 'Love is Blind',
                                 'How would you rate Sex Education?' : 'Sex Education',
                                 'How would you rate The Witcher? ' : 'The Witcher',
                                 'How would you rate Stranger Things?' : 'Stranger Things',
                                 'How would you rate Russian Doll?' : 'Russian Doll',
                                 'How would you rate Pose?' : 'Pose',
                                 'How would you rate "Other"?' : 'Other'})\
                .melt(id_vars=['Timestamp', 'name', 'device used', 'shows watched'],
                      value_vars=['Tiger King', 'Community', 'Brooklyn Nine-Nine', 'Love is Blind', 'Pose', 'Sex Education', 'The Witcher', 'Stranger Things', 'Russian Doll', 'Other'],
                      value_name='rating',
                      var_name='show rated')
df_devices = pd.read_excel('PD 2020W17 Shows and Devices (1).xlsx', sheet_name='Devices')

df_output_1 = df_survey[['name', 'device used']].drop_duplicates().copy()
device_list = list(df_devices.Device.str.lower())
string_to_remove = '|'.join(device_list)
for device in device_list:
    df_output_1[f'{device}'] = df_output_1['device used'].str.lower().str.match(f'.*?({device[0].lower()}.*?{device[-1].lower()}).*?', case=False)
df_output_1['Other'] = df_output_1['device used'].str.lower().str.replace(string_to_remove, '', regex=True)

df_output_1 = df_output_1.melt(id_vars=['name','device used'], value_vars=device_list, value_name='device used?', var_name='device').groupby('device')['device used?'].sum()


shows_to_remove = '|'.join(list(df_survey['show rated'].unique()))
df_survey['other'] = df_survey['shows watched'].str.lower().str.replace(shows_to_remove+'|,', '', regex=True, case=False).str.strip()
df_other_show_ranks = df_survey.loc[df_survey['show rated'] == 'Other'].groupby('other')['rating'].mean()
df_show_ranks = df_survey.loc[df_survey['show rated'] != 'Other'].dropna().groupby('show rated')['rating'].mean()
show(df_survey,df_show_ranks, df_other_show_ranks)