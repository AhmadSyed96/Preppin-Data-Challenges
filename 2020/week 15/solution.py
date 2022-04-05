import pandas as pd
import numpy as np
from pandasgui import show

df = pd.read_excel('Transactions (1).xlsx')\
       .assign(Items_List = lambda dfx : dfx['Items'].str.split(', '))\
       .explode('Items_List').rename(columns={'Items_List' : 'Item'})

df_expanded = pd.merge(df, df, on='TransactionID')\
                .query('Item_x != Item_y')[['TransactionID','Items_x', 'Item_x', 'Item_y']]\
                .rename(columns={'Items_x':'Items', 'Item_x':'LHS Item', 'Item_y':'RHS Item'})\
                .assign(Total_Transactions = lambda dfx : dfx.TransactionID.nunique(),
                        LHS_Apperence_Count = lambda dfx : dfx.groupby('LHS Item')['TransactionID'].transform('nunique'),
                        RHS_Apperence_Count = lambda dfx : dfx.groupby('RHS Item')['TransactionID'].transform('nunique'),
                        OVR_Apperence_Count = lambda dfx : dfx.groupby(['LHS Item', 'RHS Item'])['TransactionID'].transform('nunique'),
                        LHS_Support = lambda dfx : dfx.LHS_Apperence_Count / dfx.Total_Transactions,
                        RHS_Support = lambda dfx : dfx.RHS_Apperence_Count / dfx.Total_Transactions,
                        Confidence = lambda dfx : dfx.OVR_Apperence_Count / dfx.LHS_Apperence_Count,
                        Lift = lambda dfx : (dfx.OVR_Apperence_Count / dfx.Total_Transactions)/(dfx.LHS_Support * dfx.RHS_Support))

