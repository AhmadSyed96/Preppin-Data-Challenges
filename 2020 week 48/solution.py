import pandas as pd
from pandasgui import show
import numpy as np

df_stands = pd.read_excel('2020W48 Input.xlsx', sheet_name='Stands')\
              .assign(Gate = lambda dfx : dfx['Accessed by Gates'].str.split(','))\
              .drop(columns=['Accessed by Gates'])\
              .explode('Gate')\
              .assign(Gate = lambda dfx : dfx['Gate'].str.replace('G',''),
                      Stand = lambda dfx : dfx['Stand'].str.replace('S',''))
df_time_to_remote = pd.read_excel('2020W48 Input.xlsx', sheet_name='Remote Stands Accesibility')\
                .assign(Gate = lambda dfx : dfx['Gate'].str[-1])

df_flights = pd.read_excel('2020W48 Input.xlsx', sheet_name=2)\
                 .assign(arrival = lambda dfx : pd.to_datetime('2020-02-01' + dfx['Time'].astype('string'), format='%Y-%m-%d%H%M'),
                         departure =  lambda dfx : dfx['arrival'] + pd.Timedelta(minutes=45),
                         Stand = lambda dfx : dfx['Stand'].astype('string'))

df_Gate_Avail = pd.read_excel('2020W48 Input.xlsx', sheet_name=3)\
                  .rename(columns={'Date':'Open Time Slot'})\
                  .assign(Gate = lambda dfx : dfx['Gate'].astype('string'))

df_possible_combos = df_flights.merge(df_stands, how='left', on='Stand')\
                                 .merge(df_time_to_remote, how='left', on=['Gate'])\
                                 .merge(df_Gate_Avail, how='left', on='Gate')\
                                 .query('`Open Time Slot`>= arrival and `Open Time Slot` < departure')\
                                 .assign(Gates_Available = lambda dfx : dfx.groupby('Flight')['Gate'].transform('nunique'),
                                         Flight_Number = lambda dfx : dfx['Flight'].str.extract('(\d+)'))\
                                 .reset_index(drop=True)

# get priority 1 from the possible gate flight combos
df_priority_1 = df_possible_combos.query('Gates_Available == 1')
df_priority_1 = df_priority_1[['Flight', 'Stand', 'Gate', 'Open Time Slot', 'Requires Bus?']]


#take those pairs out from the possible combos
df_possible_combos = df_possible_combos.merge(df_priority_1, on=['Flight'], how='outer', indicator=True).query('_merge=="left_only"')
df_possible_combos = df_possible_combos.loc[:,~df_possible_combos.columns.str.endswith('_y')].drop(columns=['_merge']).rename(columns=lambda x : x.replace('_x', ''))
df_possible_combos = df_possible_combos.merge(df_priority_1, on=['Gate', 'Open Time Slot'], how='outer', indicator=True).query('_merge=="left_only"')
df_possible_combos = df_possible_combos.loc[:,~df_possible_combos.columns.str.endswith('_y')].drop(columns=['_merge']).rename(columns=lambda x : x.replace('_x', ''))

# get priority 2
df_priority_2 = df_possible_combos.loc[df_possible_combos['Requires Bus?'] == 'Y']
df_priority_2['minimum travel time'] = df_priority_2.groupby('Flight')['Time to Reach Remote Stands'].transform('min')
df_priority_2 = df_priority_2.loc[df_priority_2['Time to Reach Remote Stands'] == df_priority_2['minimum travel time']]
df_priority_2 = df_priority_2[['Flight', 'Stand', 'Gate', 'Open Time Slot', 'Requires Bus?']]


#take those pairs out from the possible combos
df_possible_combos = df_possible_combos.merge(df_priority_2, on=['Flight'], how='outer', indicator=True).query('_merge=="left_only"')
df_possible_combos = df_possible_combos.loc[:,~df_possible_combos.columns.str.endswith('_y')].drop(columns=['_merge']).rename(columns=lambda x : x.replace('_x', ''))
df_possible_combos = df_possible_combos.merge(df_priority_2, on=['Gate', 'Open Time Slot'], how='outer', indicator=True).query('_merge=="left_only"')
df_possible_combos = df_possible_combos.loc[:,~df_possible_combos.columns.str.endswith('_y')].drop(columns=['_merge']).rename(columns=lambda x : x.replace('_x', ''))

#assign the rest of the flights to gates with the hightest transport time to remote stands
df_possible_combos['maximum travel time'] = df_possible_combos.groupby('Flight')['Time to Reach Remote Stands'].transform('max')
df_priority_3 = df_possible_combos.loc[df_possible_combos['Time to Reach Remote Stands'] == df_possible_combos['maximum travel time']]
df_priority_3['gate count'] = df_priority_3.groupby(['Gate', 'Time'])['Flight'].transform('nunique')
df_priority_4 = df_priority_3.loc[df_priority_3['gate count'] == 2]
df_priority_3 = df_priority_3.loc[df_priority_3['gate count'] == 1]
df_priority_3 = df_priority_3[['Flight', 'Stand', 'Gate', 'Open Time Slot', 'Requires Bus?']]

#take those pairs out from the possible combos
df_possible_combos = df_possible_combos.merge(df_priority_3, on=['Flight'], how='outer', indicator=True).query('_merge=="left_only"')
df_possible_combos = df_possible_combos.loc[:,~df_possible_combos.columns.str.endswith('_y')].drop(columns=['_merge']).rename(columns=lambda x : x.replace('_x', ''))
df_possible_combos = df_possible_combos.merge(df_priority_3, on=['Gate', 'Open Time Slot'], how='outer', indicator=True).query('_merge=="left_only"')
df_possible_combos = df_possible_combos.loc[:,~df_possible_combos.columns.str.endswith('_y')].drop(columns=['_merge']).rename(columns=lambda x : x.replace('_x', ''))


#deal with ties
df_priority_4['priority flight'] = df_priority_4.groupby('Gate')['Flight_Number'].transform('min')
df_priority_4 = df_priority_4.loc[df_priority_4['Flight_Number'] == df_priority_4['priority flight']]
df_priority_4 = df_priority_4[['Flight', 'Stand', 'Gate', 'Open Time Slot', 'Requires Bus?']]


#take those pairs out from the possible combos
df_possible_combos = df_possible_combos.merge(df_priority_4, on=['Flight'], how='outer', indicator=True).query('_merge=="left_only"')
df_possible_combos = df_possible_combos.loc[:,~df_possible_combos.columns.str.endswith('_y')].drop(columns=['_merge']).rename(columns=lambda x : x.replace('_x', ''))
df_possible_combos = df_possible_combos.merge(df_priority_4, on=['Gate', 'Open Time Slot'], how='outer', indicator=True).query('_merge=="left_only"')
df_possible_combos = df_possible_combos.loc[:,~df_possible_combos.columns.str.endswith('_y')].drop(columns=['_merge']).rename(columns=lambda x : x.replace('_x', ''))

#keep only from possibilities df
df_possible_combos = df_possible_combos[['Flight', 'Stand', 'Gate', 'Open Time Slot', 'Requires Bus?']]

#concat
df_flight_allocations = pd.concat([df_priority_1, df_priority_2, df_priority_3, df_priority_4, df_possible_combos])

#merge with all gate times
df_output = df_Gate_Avail.merge(df_flight_allocations, how='outer', on=['Gate', 'Open Time Slot']).merge(df_time_to_remote, how='left', on=['Gate'])
df_output['Time to Reach Remote Stands'] = np.where(df_output['Requires Bus?']=='Y', df_output['Time to Reach Remote Stands'], np.nan)
df_output['flight per gate-time'] = df_output.groupby(['Gate', 'Open Time Slot'])['Flight'].transform('nunique')
show(df_output)