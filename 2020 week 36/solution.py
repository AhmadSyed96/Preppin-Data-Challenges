import pandas as pd
from pandasgui import show
import numpy as np

df_teachers = pd.read_excel('School Timetables-4 (1).xlsx', sheet_name='Teachers')\
                .assign(Working_Days = lambda dfx : dfx['Working Days'].str.split(','))\
                .drop(columns=['Working Days'])\
                .explode('Working_Days')\
                .assign(Classes_Taught = lambda dfx : dfx.groupby('Name')['Subject'].transform('nunique'),
                        Hours_Available = lambda dfx : 6 / dfx['Classes_Taught'])

df_students = pd.read_excel('School Timetables-4 (1).xlsx', sheet_name='Students')\
                .assign(Subject = lambda dfx : dfx['Subject'].str.split('/'))\
                .explode('Subject')\
                .groupby(['Subject', 'Age'], as_index=False).count()\
                .rename(columns={'Name':'Total Students'})

df_rooms =    pd.read_excel('School Timetables-4 (1).xlsx', sheet_name='Rooms')\
                .groupby('Subjects', as_index=False)['Capacity'].sum()\
                .rename(columns={'Subjects': 'Subject'})

df_hours =    pd.read_excel('School Timetables-4 (1).xlsx', sheet_name='Hours')\
                .assign(Start_age = lambda dfx : dfx['Age Group'].str[:2].astype('int'),
                        End_age = lambda dfx : dfx['Age Group'].str[-2:].astype('int'),
                        Range = lambda dfx : dfx[['Start_age', 'End_age']].apply(lambda x: list(range(x.Start_age, x.End_age+1)), axis=1))\
                .explode('Range')[['Range', 'Hours teaching per week']].rename(columns={'Range':'Age', 'Hours teaching per week':'Hours Required per'})

df_output =   pd.merge(df_students, df_rooms, on='Subject')\
                .assign(Rooms_Needed = lambda dfx : np.ceil(dfx['Total Students']  /  dfx['Capacity']))\
                .merge(df_hours, how='left', on='Age')\
                .assign(Hours_Required = lambda dfx : dfx['Hours Required per'] * dfx['Rooms_Needed'])\
                .groupby('Subject').agg({'Rooms_Needed':'sum', 'Hours_Required':'sum'})\
                .merge(df_teachers.groupby('Subject')['Hours_Available'].sum(), how='left', on='Subject')\
                .assign(percent_utilized = lambda dfx : dfx['Hours_Required'] / dfx['Hours_Available'])

show(df_hours, df_rooms, df_students, df_teachers, df_output)