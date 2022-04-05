import pandas as pd
from pandasgui import show
import datetime

exch_rates = pd.read_excel('PD 2020 Wk 6 Input (1).xlsx',sheet_name=0)


exch_rates['Week'] = [int(d.strftime('%U'))+1 for d in exch_rates['Date']]
exch_rates['Year'] = [d.year for d in exch_rates['Date']]
exch_rates['Rate'] = exch_rates['British Pound to US Dollar'].str.extract('.*=\s(\d\.\d*).*').astype('float')
print(exch_rates)

HL_rates_per_week = exch_rates.groupby(['Week', 'Year'])['Rate'].agg([('max rate','max'),('min rate','min')]).reset_index()
print(HL_rates_per_week)


sales = pd.read_excel('PD 2020 Wk 6 Input (1).xlsx',sheet_name=1)
sales['UK Sales Value(GBP)'] = sales['Sales Value'] - (sales['Sales Value']*sales['US Stock sold (%)']*0.01)
print(sales)

combined_df = sales.merge(HL_rates_per_week, how='left', on=['Week', 'Year'])
combined_df['US Sales Best Value'] = combined_df['Sales Value']*combined_df['US Stock sold (%)']*0.01*combined_df['max rate']
combined_df['US Sales Worst Value'] = combined_df['Sales Value']*combined_df['US Stock sold (%)']*0.01*combined_df['min rate']
combined_df['variance'] = combined_df['US Sales Best Value'] - combined_df['US Sales Worst Value']
print(combined_df)