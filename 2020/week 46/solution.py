import pandas as pd
from pandasgui import show

df = pd.read_excel('Incident List.xlsx', sheet_name='Incident List')
df[['split' ,'Incident clean']] = df['Incident'].str.rsplit(', ', n=1, expand=True)
df['split'] =df['split'].replace({' on ':'; ', ' at ':'; ', ' near ':'; '}, regex=True)
df[['Aircraft', 'Location', 'Date']] = df['split'].str.split('; ' ,expand=True)
# show(df)

###can NOT figure out output 2