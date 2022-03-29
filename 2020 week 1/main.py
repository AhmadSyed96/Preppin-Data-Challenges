# import pandas as pd
# import numpy as np
# df = pd.read_csv('PD 2020 WK 1 Input - Sheet1.csv')
#
#
# hierarchy = df['Item'].str.split(' ', n=0, expand=True)[0]
# hierarchy_split = hierarchy.str.split('.', expand=True)
# df[sorted(hierarchy_split)] = hierarchy.str.split('.', expand=True)
# df = df[[0,1,2,"Item","Profit"]]
# # print(df)
#
#
# Item_X_Profit = df.groupby(0)["Profit"].sum()
# # print(Item_X_Profit)
#
# df = df.join(Item_X_Profit,on=0,how="left",rsuffix="r",lsuffix="l")
# # print(df)
#
# # df = pd.merge(df[["Profitl"]],df[['Profitr']],how='left')
# # df['Profit'] = df['Profitl'].fillna(df['Profitr'])
# df['Profit'] = np.where(df[1]=="",df['Profitr'],df['Profitl'])
# # print(df)
#
# Item_XX_Profit = df.groupby([0,1])['Profitl'].sum()
# # print(Item_XX_Profit)
# df = df.join(Item_XX_Profit,on=[0,1],how="left",rsuffix="r",lsuffix="l")
# # print(df)
#
# df['Profit'] = df['Profit'].fillna(df['Profitlr'])
# df = df.drop(['Profitll','Profitr','Profitlr'],axis=1)
# # print(df)
#
#
# df['number count'] = df.Item.str.count('\d')
# df['Item'] = [" "*5*x for x in df['number count']-1]+df.Item
# df = df[['Item','Profit']]
# print(df)



import pandas as pd

# read in the file
df = pd.read_csv('PD 2020 WK 1 Input - Sheet1.csv')

# replace nulls with zeroes
df['Profit'].fillna(0, inplace=True)

# extract the hierarchy from the Item and copy it
df['Hierarchy'] = df['Item'].str.extract('([\d\.]+?)\.? .*')
df['Hierarchy2'] = df['Hierarchy']
print(df)
df['Level'] = df['Hierarchy'].str.count('\.')
print(df['Level'])

maxLevel = df['Level'].max()
print(maxLevel)

# iterate through the hierarchy levels, creating subtotals at each level
dfSubtotal = None
for i in range(maxLevel, 0, -1):
    # remove a layer of hierarchy
    df['Hierarchy2'] = df['Hierarchy2'].str.extract('(.*?)\.\d+$')
    print(df)

    # using only the detail records, sum by current level of hierarchy
    # and add to the Subtotal df
    dfSubtotal = pd.concat([dfSubtotal,
                            df[df['Level'] == maxLevel].groupby(df['Hierarchy2'], as_index=True)['Profit'].sum()])
    print(dfSubtotal)
# join subtotals back to the main dataframe and update the Profit
df = pd.merge(df, dfSubtotal, how='left', left_on='Hierarchy', right_index=True)
print(df)
df['Profit'] = df['Profit_x'] + df['Profit_y'].fillna(0)

# add the spacing to the Item
df['Item'] = [' ' * 5 * x for x in df['Level']] + df['Item']

# clean up columns
df = df[['Item', 'Profit']]
print(df)

