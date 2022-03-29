import pandas as pd
from pandasgui import show

df_internal = pd.read_excel('Matching.xlsx', sheet_name='Internal Data')
df_3rd_party = pd.read_excel('Matching.xlsx', sheet_name='3rd Party Data')

df_matched_on_ID = pd.merge(df_internal, df_3rd_party, left_on='ID', right_on='3rd Party ID')\
                     .drop(columns=['Scent_y'])\
                     .rename(columns={'Sales' : 'Internal Sales', 'Scent_x' : 'Scent', 'ID' : 'Internal ID'})\
                     .assign(Status = 'Matched on ID')
df_3rd_unmatched = pd.merge(df_internal, df_3rd_party, how="outer", indicator=True, left_on='ID', right_on='3rd Party ID')\
                     .query('_merge=="right_only"')\
                     .drop(columns=['_merge', 'ID', 'Scent_x', 'Sales'])\
                     .rename(columns={'Scent_y':'Scent'})
df_internal_unmatched = pd.merge(df_internal, df_3rd_party, how="outer", indicator=True, left_on='ID', right_on='3rd Party ID')\
                          .query('_merge=="left_only"')\
                          .drop(columns=['_merge', '3rd Party ID', 'Scent_y', '3rd Party Sales'])\
                          .rename(columns={'Scent_x':'Scent', 'Sales' : 'Internal Sales', 'ID' : 'Internal ID'})
# show(df_matched, df_3rd_unmatched, df_internal_unmatched)

df_matched_on_scent = pd.merge(df_internal_unmatched, df_3rd_unmatched, how='left', on='Scent')\
                                   .assign(Status='Matched on Scent',
                                           Absolute_Sales_Difference =
                                                lambda dfx : abs(dfx['Internal Sales'] - dfx['3rd Party Sales']),
                                           Minimum_3rd =
                                                lambda dfx : dfx.groupby('3rd Party ID')['Absolute_Sales_Difference']
                                                                .transform('min'))\
                                   .query('Absolute_Sales_Difference == Minimum_3rd')\
                                   .assign(Minimum_Internal =
                                                lambda dfx : dfx.groupby('Internal ID')['Absolute_Sales_Difference'].transform('min'))\
                                   .query('Absolute_Sales_Difference == Minimum_Internal')\
                                   .drop(columns=['Absolute_Sales_Difference', 'Minimum_3rd', 'Minimum_Internal'])

df_3rd_unmatched = df_3rd_unmatched.merge(df_matched_on_scent,
                                          how='outer',
                                          on='3rd Party ID',
                                          indicator=True)\
                                    .query('_merge=="left_only"')\
                                    .drop(columns=['Internal ID', 'Scent_y', 'Internal Sales', '3rd Party Sales_y', 'Status', '_merge'])\
                                    .rename(columns={'Scent_x':'Scent', '3rd Party Sales_x':'3rd Party Sales'})\
                                    .assign(Status = '3rd party unmatched')
df_internal_unmatched = df_internal_unmatched.merge(df_matched_on_scent,
                                                    how='outer',
                                                    on='Internal ID',
                                                    indicator=True)\
                                             .query('_merge=="left_only"')\
                                             .drop(columns=['Scent_y', 'Internal Sales_y', '3rd Party ID', '3rd Party Sales', 'Status', '_merge'])\
                                             .rename(columns={'Scent_x':'Scent', 'Internal Sales_x':'Internal Sales'})\
                                             .assign(Status = 'internal unmatched')


df_output = pd.concat([df_matched_on_ID, df_matched_on_scent, df_3rd_unmatched, df_internal_unmatched])
show(df_output)

