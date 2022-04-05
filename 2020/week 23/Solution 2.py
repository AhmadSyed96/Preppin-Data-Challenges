import pandas as pd
from pandasgui import show

df_attempts =  pd.read_excel('Quiz Results (1).xlsx',sheet_name='Participant Answers')\
                .melt(id_vars=['Name'],
                      value_vars=['Round1', 'Round2', 'Round3', 'Round4', 'Round5'],
                      var_name='Round',
                      value_name='Attempt')\
                .assign(Attempt = lambda dfx : dfx['Attempt'].str.strip().str.split(','))\
                .explode('Attempt').reset_index(drop=True)\
                .assign(Question = lambda dfx : dfx.groupby(['Name', 'Round']).cumcount()+1)\
                .pivot(index=['Name', 'Question'], columns='Round', values='Attempt')

df_answer = pd.read_excel('Quiz Results (1).xlsx',sheet_name='Correct Answers')\
               .assign(Answers = lambda dfx : dfx['Answers'].str.strip().str.split(','))\
               .explode('Answers').reset_index(drop=True)\
               .assign(Question = lambda dfx : dfx.groupby('Round').cumcount()+1)\
               .pivot(index='Question', columns='Round', values='Answers')


df_output = None
for pair,attempts in df_attempts.groupby(level=0):
    df_output = pd.concat([df_output, attempts.eq(df_answer)])
df_output = df_output.groupby(level=0).sum()
df_output['Total Score'] = df_output.sum(axis=1)
df_output['Rank'] = df_output['Total Score'].rank(ascending=False, method='dense')
df_output = df_output.sort_values(by=['Rank'])
show(df_output)