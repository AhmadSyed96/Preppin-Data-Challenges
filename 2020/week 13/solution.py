import pandas as pd
from pandasgui import show
import numpy as np

with pd.ExcelFile('Ticket Data_Updated.xlsx') as xl:
    df_tickets = pd.concat([pd.read_excel(xl, s) for s in xl.sheet_names if 'SLA' not in s])
    df_deadline = pd.read_excel(xl, sheet_name='SLA Agreements')

# show(df_tickets)

df_tickets[['Ticket ID', 'Department']] = df_tickets.Ticket.str.extract('(.*)\s\/\s(.*)\s\/.*')
# df_tickets['Department'] = df_tickets['Department'].replace(' ','')
df_tickets.drop(columns='Ticket', inplace=True)


df_tickets['Day'] = df_tickets['Timestamp'].dt.strftime('%A')
df_tickets['Day Type'] = np.where((df_tickets['Day']=='Saturday')|(df_tickets['Day']=='Sunday'),'Weekend','Weekday')
# show(df_tickets)

bd = pd.tseries.offsets.BusinessDay(n = 1)
df_tickets['New Timestamp'] = np.where((df_tickets['Day Type'] == 'Weekend') & (df_tickets['Status Name']=='Logged'), df_tickets['Timestamp']+bd, np.where((df_tickets['Day Type'] == 'Weekend') & (df_tickets['Status Name']=='Closed'), df_tickets['Timestamp']-bd, df_tickets['Timestamp']))
# show(df_tickets)

df_tickets['Latest TS per Ticket'] = df_tickets.groupby('Ticket ID')['New Timestamp'].transform('max')
df_tickets['First TS per Ticket'] = df_tickets.groupby('Ticket ID')['New Timestamp'].transform('min')



A = [d.date() for d in df_tickets['First TS per Ticket']]
B = [d.date() for d in df_tickets['Latest TS per Ticket']]
df_tickets['Days Open'] = np.busday_count(A,B)
# df_tickets['Days Open'] = df_tickets['Days Open'].astype('int')
# df_current_status = df_tickets.groupby('Ticket ID')['Timestamp'].max().reset_index()

current_tickets = np.where(df_tickets['New Timestamp'] == df_tickets['Latest TS per Ticket'])
df_current_tickets = df_tickets.iloc[current_tickets].merge(df_deadline, on='Department', how='left')
# show(df_current_tickets)

df_status_count = df_tickets[df_tickets['Timestamp'] == df_tickets.groupby('Ticket ID')['Timestamp'].transform('max')][['Status Name','Ticket ID']].groupby('Status Name',as_index=False)['Ticket ID'].count().rename(columns={'Status Name':'Latest Status'})
# show(df_status_count)
# show(df_current_status, df_tickets)




closed = df_current_tickets['Status Name']=='Closed'
open = df_current_tickets['Status Name']!='Closed'
over_SLA = df_current_tickets['Days Open'] > df_current_tickets['SLA Agreement']
under_SLA = df_current_tickets['Days Open'] <= df_current_tickets['SLA Agreement']



df_closed_over = df_current_tickets[closed & over_SLA].groupby('Status Name',as_index=False)['Ticket ID'].count().rename(columns={'Status Name':'Metric', 'Ticket ID':'Total'})
df_open_under = df_current_tickets[open & under_SLA]
df_open_under['Status Name'] = 'Open under SLA'
df_open_under = df_open_under.groupby('Status Name',as_index=False)['Ticket ID'].count().rename(columns={'Status Name':'Metric', 'Ticket ID':'Total'})
show(df_open_under, df_closed_over)


df_closed = df_current_tickets[closed]
df_closed['SLA met?'] = np.where(df_closed['Days Open'] <= df_closed['SLA Agreement'],1,0)
# show(df_closed)

df_closed_agg = df_closed.groupby('Department',as_index=False).agg({'SLA met?':'sum', 'Ticket ID':'count'}).rename(columns={'SLA met?':'Total Closed', 'Ticket ID':'Total Tickets'})
# show(df_closed_agg)
df_closed_agg['SLA met %'] = df_closed_agg['Total Closed'] / df_closed_agg['Total Tickets']
df_closed_agg['Rank'] = df_closed_agg['SLA met %'].rank(method='dense', ascending=False)
show(df_closed_agg)

