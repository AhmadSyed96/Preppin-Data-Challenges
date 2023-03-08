bank_trans['Bank'] = bank_trans['Transaction Code'].str.extract('[A-Z]+')
bank_trans['Online or In-Person'] = bank_trans['Online or In-Person'].map({2:'Online' , 1:'In Person'})
bank_trans['Transaction Date'] = bank_trans['Transaction Date'].dt.day_name()

sol_1 = df_trans.groupby('Bank')['Value'].sum()

sol_2 = df_trans.groupby(['Bank', 'Online or In-Person', 'Transaction Date'])['Value'].sum()

sol_3 = df_trans.groupby(['Bank', 'Customer Code'])['Value'].sum()