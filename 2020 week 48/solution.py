import pandas as pd
from pandasgui import show

df_stands = pd.read_excel('2020W48 Input.xlsx', sheet_name='Stands').assign(Gate = lambda dfx : dfx['Accessed by Gates'].str.split(',')).drop(columns=['Accessed by Gates']).explode('Gate').assign(Gate = lambda dfx : dfx['Gate'].str.replace('G',''), Stand = lambda dfx : dfx['Stand'].str.replace('S',''))
df_T2Stands = pd.read_excel('2020W48 Input.xlsx', sheet_name='Remote Stands Accesibility').assign(Gate = lambda dfx : dfx['Gate'].str[-1], Bus = 'Y').rename(columns={'Bus':'Requires Bus?'})
df_Stand_Loc = pd.read_excel('2020W48 Input.xlsx', sheet_name=2).assign(arrival = lambda dfx : pd.to_datetime('2020-02-01' + dfx['Time'].astype('string'), format='%Y-%m-%d%H%M'), departure =  lambda dfx : dfx['arrival'] + pd.Timedelta(minutes=45), Stand = lambda dfx : dfx['Stand'].astype('string')).drop(columns=['Time'])
df_Gate_Avail = pd.read_excel('2020W48 Input.xlsx', sheet_name=3).rename(columns={'Date':'Open Time Slot'}).assign(Gate = lambda dfx : dfx['Gate'].astype('string'))

df_output = df_Stand_Loc.merge(df_stands, how='left', on='Stand').merge(df_T2Stands, how='left', on=['Gate', 'Requires Bus?']).merge(df_Gate_Avail, how='left', on='Gate')
# show(df_stands, df_T2Stands, df_Stand_Loc, df_Gate_Avail, df_output)
df_output = df_output[(df_output['Open Time Slot'] >= df_output['arrival']) & (df_output['Open Time Slot'] < df_output['departure'])]