import pandas as pd
from pandasgui import show


wb1 = pd.read_excel('Updating Weather data (2).xlsx', sheet_name=None,names=['data'], header=None)
all_sheets = []
for name, sheet in wb1.items():
    sheet['Forcast'] = name
    if 'Days' in name:
        sheet[['Date or Time', 'Min Temp', 'Max Temp', 'Percipitation Chance']] = sheet['data'].str.split('\n', expand=True)
    else:
        sheet[['Date or Time', 'Temperature', 'Percipitation Chance']] = sheet['data'].str.split('\n', expand=True)
    all_sheets.append(sheet)

full_table = pd.concat(all_sheets)
full_table.reset_index(inplace=True, drop=True)

