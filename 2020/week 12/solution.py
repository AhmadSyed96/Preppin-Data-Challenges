import pandas as pd
from pandasgui import show

with pd.ExcelFile('PD week 12 input (1) (1).xlsx') as xl:
    df_total_sales = pd.read_excel(xl,sheet_name='Total Sales')
    df_pct_sales = pd.read_excel(xl, sheet_name='Percentage of Sales')
    df_lookup = pd.read_excel(xl, sheet_name='Lookup Table')

volumes = df_pct_sales['Size'].unique()
volumes_string = '|'.join(volumes)
df_lookup['Product ID'] = df_lookup['Product'].str.replace(volumes_string, '', regex=True)
df_lookup.drop(columns='Product', inplace=True)
df_lookup['Scent'] = df_lookup['Scent'].str.replace('\s','').str.title()
df_lookup.drop_duplicates(inplace=True)
print(df_lookup)

df_pct_sales['Week Number'] = df_pct_sales['Week Commencing'].dt.strftime('%U').astype('int')+1
df_pct_sales['Year'] = [d.year for d in df_pct_sales['Week Commencing']]
print(df_pct_sales)
#
df_total_sales['Year'] = df_total_sales['Year Week Number'].astype('string').str[:4].astype('int')
df_total_sales['Week Number'] = df_total_sales['Year Week Number'].astype('string').str[-2:].astype('int')
df_total_sales['Scent'] = df_total_sales['Scent'].str.replace('\s','').str.title()
print(df_total_sales)

df_pct_w_lookup = df_pct_sales.merge(df_lookup, on=['Product ID'], how='left')
# show(df_pct_w_lookup, df_pct_sales, df_lookup)
df_sales_per = df_pct_w_lookup.merge(df_total_sales, on=['Year', 'Week Number', 'Scent'], how='left')
# show(df_sales_per)

df_sales_per['Sales'] = df_sales_per['Percentage of Sales'] * df_sales_per['Total Scent Sales']
df_sales_per['Year Week Number'] = df_sales_per['Year Week Number'].astype('string')
df_sales_per = df_sales_per[['Year Week Number', 'Scent', 'Size', 'Product Type', 'Sales']]
show(df_sales_per)