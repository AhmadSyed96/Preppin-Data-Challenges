import pandas as pd
from pandasgui import show

df_attempts = pd.read_excel('Quiz Results (1).xlsx',sheet_name='Participant Answers')\
                .melt(id_vars=['Name'],
                      value_vars=['Round1', 'Round2', 'Round3', 'Round4', 'Round5'],
                      var_name='Round',
                      value_name='Attempt')\
                .assign(Attempt = lambda dfx : dfx['Attempt'].str.strip().str.split(','))\
                .explode('Attempt').reset_index(drop=True)\
                .assign(Question = lambda dfx : dfx.groupby(['Name', 'Round']).cumcount()+1)

df_answers = pd.read_excel('Quiz Results (1).xlsx',sheet_name='Correct Answers')\
               .assign(Answers = lambda dfx : dfx['Answers'].str.strip().str.split(','))\
               .explode('Answers').reset_index(drop=True)\
               .assign(Question = lambda dfx : dfx.groupby('Round').cumcount()+1)

df_output = pd.merge(df_attempts, df_answers, on=['Round', 'Question'], how='left')\
              .assign(Correct = lambda dfx : dfx['Attempt'] == dfx['Answers'])\
              .groupby(['Name', 'Round'], as_index=False, sort=False)['Correct'].sum()\
              .pivot(index='Name', columns='Round', values='Correct')
show(df_output)

