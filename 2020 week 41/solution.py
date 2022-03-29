import pandas as pd
from pandasgui import show
import numpy as np

df_comments = None
with pd.ExcelFile('Prep Tips live chat logs.xlsx') as xl:
    df_comments = pd.concat([pd.read_excel(xl, s).assign(Region = s.replace(' Session', ''), Time = lambda dfx : pd.to_datetime(dfx['Time'].astype(str))) for s in xl.sheet_names])

df_output_1 =  pd.merge(df_comments, df_comments.groupby('Who', as_index=False)['Time'].min().query('Who != "Carl Allchin"'), on=['Who', 'Time'])[['Who' ,'Comment', 'Region']].assign(City = lambda dfx : dfx['Comment'].str.title().str.extract('(.*)\,.*'), Country = lambda dfx : dfx['Comment'].str.title().str.extract('.*\,\s(\w*)\.?.*?'), first_time = lambda dfx : dfx['Comment'].str.contains('first time', case=False)).drop(columns=['Comment'])
# show(df_output_1)

df_output_2 = pd.merge(df_comments, df_comments.groupby('Who', as_index=False)['Time'].min(), on=['Who', 'Time'], how='outer', indicator = True).query('_merge != "both"').assign(QorA = lambda dfx : np.where(dfx['Comment'].str.contains('?', regex=False), 'Question', 'Answer')).groupby(['Region', 'QorA'])['Comment'].count()
show(df_output_2)