import pandas as pd

df_key = pd.read_excel('2020W20 Input (1).xlsx', sheet_name='Cipher', index_col='Cipher')['Alphabet'].to_dict()
df_cipher = pd.read_excel('2020W20 Input (1).xlsx', sheet_name='Encrypted Message')


df_decryptions = df_cipher.assign(Decrypted = lambda dfx : dfx['Encrypted Message']
                            .apply(list))\
                            .explode('Decrypted')\
                            .replace(df_key)\
                            .groupby('Encrypted Message')\
                            .agg({'Decrypted': lambda x: ''.join(x.tolist())})\
                            .reset_index(level=0)
