import pandas as pd
from pandasgui import show
import numpy as np
import sweetviz as sv

#Filter out any specimen that doesn't have a measurement for each trait or those with '*'s against measurements.
convert_dict = {'Total_body_length' : 'float', 'Prosoma_length' : 'float','Prosoma_width' : 'float','Prosoma_height' : 'float', 'Tibia_I_length' : 'float', 'Fang_length' : 'float'}
df = pd.read_csv('PD Week 14 Input.csv').replace({'_': np.nan}).dropna().drop(columns=['Code', 'Family', 'Location']).reset_index(drop=True)

ast_cols = ['Total_body_length','Prosoma_length' ,'Prosoma_width' ,'Prosoma_height' ,'Tibia_I_length','Fang_length']
ast_rows = np.column_stack([df[col] .str.contains('\*') for col in ast_cols])
df = df.loc[~ast_rows.any(axis=1)].reset_index(drop=True)


df[ast_cols] = df[ast_cols].apply(pd.to_numeric, errors='coerce', axis=1)


df['Species Count'] = df.groupby('Species')['Species'].transform('count')
df = df[df['Species Count'] >= 10]

# print(df.columns.values)
df_unpvt = df.melt(id_vars=['Species', 'Sex'], value_vars = ast_cols, var_name='Trait')
# show(df_unpvt)

df_unpvt['Avg'] = df_unpvt.groupby('Species')['value'].transform('mean')
df_unpvt['Min'] = df_unpvt.groupby('Species')['value'].transform('min')
df_unpvt['Max'] = df_unpvt.groupby('Species')['value'].transform('max')
df_unpvt['Norm val'] = df_unpvt.groupby('Species')['value'].transform(lambda x: (x - x.min()) / (x.max() - x.min()))
# print(df_unpvt.dtypes)
show(df_unpvt)


# convert_dictadvert_report = sv.analyze(df)#display the report
# advert_report.show_html('Advertising.html')