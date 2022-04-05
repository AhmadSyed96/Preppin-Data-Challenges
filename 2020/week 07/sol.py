import pandas as pd
from pandasgui import show

reporting_date_df = pd.read_csv('PD 2020 Wk 7 Reporting Date Input (1).csv', parse_dates=['Month'])
terminated_emps_df = pd.read_csv('PD 2020 Wk 7 Leavers Input (1).csv',parse_dates=['Join Date', 'Leave Date'])
current_emps_df = pd.read_csv('PD 2020 Wk 7 Current Employees Input (1).csv',parse_dates=['Join Date'])

current_emps_df['Join Month'] = current_emps_df['Join Date'].dt.strftime('%Y-%m-1').astype('datetime64[ns]')
terminated_emps_df['Join Month'] = terminated_emps_df['Join Date'].dt.strftime('%Y-%m-1').astype('datetime64[ns]')
terminated_emps_df['Leave Month'] = terminated_emps_df['Leave Date'].dt.strftime('%Y-%m-1').astype('datetime64[ns]')

terminated_emps_df['dummy'] = 1
current_emps_df['dummy'] = 1
reporting_date_df['dummy'] = 1
months_per_termindated_df = pd.merge(terminated_emps_df, reporting_date_df, on='dummy')
months_per_termindated_df = months_per_termindated_df[(months_per_termindated_df['Join Month']<=months_per_termindated_df['Month'])&(months_per_termindated_df['Leave Month']>months_per_termindated_df['Month'])]
months_per_current_df = pd.merge(current_emps_df, reporting_date_df, on='dummy')
months_per_current_df = months_per_current_df[months_per_current_df['Join Month']<=months_per_current_df['Month']]

all_emps_per_month_df = pd.concat([months_per_termindated_df,months_per_current_df]).drop('dummy',1)
all_emps_per_month_df['Salary'] = all_emps_per_month_df['Salary'].astype('string').str.replace('[\D]','').astype('int')
# show(all_emps_per_month_df)

monthly_salary_df = all_emps_per_month_df.groupby('Month',as_index=False).agg({'Employee ID':'count', 'Salary':'sum'})
monthly_salary_df.columns = ['Month', 'Current Employees', 'Salary']
monthly_salary_df['Avg Salary'] = monthly_salary_df['Salary'] / monthly_salary_df['Current Employees']
show(monthly_salary_df)
