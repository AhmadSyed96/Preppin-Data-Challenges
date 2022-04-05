import pandas as pd
import numpy as np
from pandasgui import show

def get_box_sizes(orders_df, sizes_df):

    df = orders_df.assign(Remainder=lambda df_x: df_x['Order Size'])
    sizes_df.sort(reverse=True)

    for i, s in enumerate(sizes_df):
        if i < len(sizes_df) -1:
            df[f'Boxes of {s}'] = df['Remainder'] // s
            df['Remainder'] = df['Remainder'] % s
        else:
            df[f'Boxes of {s}'] = (np.ceil(df['Remainder'] / s)).astype('int')
            df['Remainder'] = (np.ceil(df['Remainder'] / s)).astype('int') * s - df['Remainder']
    return df.drop(columns=['Order Size'])

with pd.ExcelFile('PD 2020 Week 11 Input (1).xlsx') as xl:
    df_orders = pd.read_excel(xl, sheet_name='Orders')
    df_sizes = pd.read_excel(xl, sheet_name='Box Sizes')

df_boxes_per_order = pd.concat([df_orders, get_box_sizes(df_orders[['Order Size']], list(df_sizes['Box Size']))], axis=1)
# print(df_boxes_per_order)

df_soaps_per_box = df_boxes_per_order.melt(id_vars=['Order Number', 'Order Size', 'Remainder'], var_name='Box Size', value_name='Last Box Per Box Size')\
                                    .assign(Box_Number=lambda df_x:[range(1,c+1) for c in df_x['Last Box Per Box Size']],
                                            Box_Size=lambda df_x: df_x['Box Size'].str.replace('Boxes of ', '').astype(int))\
                                    .explode('Box_Number')\
                                    .dropna(subset=['Box_Number'])\
                                    .assign(Total_Boxes=lambda df_x: df_x.groupby('Order Number')['Order Number'].transform('count')).drop(columns='Box Size')
df_soaps_per_box['Box_Number'] = df_soaps_per_box['Box_Number'].astype('int')
df_soaps_per_box = df_soaps_per_box.sort_values(['Box_Size', 'Box_Number'], ascending=(False,True))
df_soaps_per_box['Box_Num'] = df_soaps_per_box.groupby('Order Number',sort=False)['Order Number'].transform('cumcount')+1
df_soaps_per_box['Soaps in Box'] = np.where(df_soaps_per_box['Box_Num']==df_soaps_per_box['Total_Boxes'],df_soaps_per_box['Box_Size'] - df_soaps_per_box['Remainder'], df_soaps_per_box['Box_Size'])
df_soaps_per_box = df_soaps_per_box.rename(columns={'Box_Num':'Box Number', 'Box_Size': 'Box Size'})
df_soaps_per_box = df_soaps_per_box[['Order Number', 'Order Size', 'Box Number', 'Box Size', 'Soaps in Box']].sort_values(by=['Order Number', 'Box Number'])
show(df_soaps_per_box)