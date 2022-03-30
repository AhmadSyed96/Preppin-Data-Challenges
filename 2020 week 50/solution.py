import pandas as pd
from pandasgui import show

df = pd.read_excel('Secret Santa.xlsx')\
    .sort_values(by='Secret Santa')\
    .assign(Santee = lambda dfx : dfx['Secret Santa'].shift(-1,fill_value='Ellie'),
            Email = lambda dfx : dfx['Email'].str.replace('\,|\!', '.', regex=True),
            Email_Body = lambda dfx : dfx['Santee'] + ", your secret santa is" + dfx['Secret Santa'] + ", good luck finding a gift")
show(df)