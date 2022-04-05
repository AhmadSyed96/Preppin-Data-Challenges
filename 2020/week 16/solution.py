import pandas as pd
from pandasgui import show

with pd.ExcelFile('Can\'t Desktop Prep this-2 (1).xlsx') as xl:
    df_sales = pd.concat([pd.read_excel(xl, s).assign(Store = s) for s in xl.sheet_names if 'Sales' in s])
    df_days_worked = pd.read_excel(xl, sheet_name='Staff days worked')

#melt the data
Sales_Columns = [cols for cols in df_sales.columns if 'Sales' in cols]
Profit_Columns = [cols for cols in df_sales.columns if 'Profit' in cols]
Other_Columns = [cols for cols in df_sales.columns if cols not in Sales_Columns+Profit_Columns]
df_sales = df_sales.melt(id_vars=Other_Columns, value_vars=Sales_Columns + Profit_Columns)

#split the variable colum that looks like 'profit 01/02/2019'
df_sales[['Type', 'Date']] = df_sales['variable'].str.split(' ', expand=True)
df_sales['Date'] = df_sales['Date'].astype('datetime64[ns]')

#make the two values n the 'type' col(profit, sales) into columns
df_sales = df_sales.pivot(index=['Category', 'Scent', 'Store', 'Date'],columns='Type', values='value').reset_index()

#group and sum up for the two new columns sales and profit
df_sales = df_sales.groupby(['Category', 'Scent', 'Store', 'Date']).agg({'Sales' : 'sum', 'Profit' : 'sum'}).reset_index()
