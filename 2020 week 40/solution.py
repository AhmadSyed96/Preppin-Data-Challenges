import pandas as pd
from pandasgui import show
from bs4 import BeautifulSoup
import re
import numpy as np


df_poems =  pd.read_excel('Wordsworth Input.xlsx', sheet_name='Wordsworth Input')\
        .replace(' ',np.nan)\
        .rename(columns={'DownloadData':'Line'})\
        .assign(filt_out = lambda dfx : dfx['Line'].str.contains('\=|\>|\<|\(', regex=True))\
        .replace('^\s*','', regex=True)\
        .replace('',np.nan, regex=True)\
        .dropna()\
        .query('filt_out == False')\
        .drop(columns=['filt_out'])\
        .replace('[^\w\s]','', regex=True)\
        .assign(Word = lambda dfx : dfx['Line'].str.split(),
                line = lambda dfx : dfx.groupby('Poem')['Line'].cumcount()+1)\
        .explode('Word')\
        .assign(word_num = lambda dfx :dfx.groupby('Line')['Word'].cumcount()+1)

df_map = pd.read_excel('Wordsworth Input.xlsx', sheet_name='Scrabble')
map_dict = dict(zip(df_map.Letter.str.lower(), df_map.Score))

df_unique_words =     pd.DataFrame(df_poems['Word']\
                        .unique(), columns=['Word'])\
                        .assign(Letter = lambda dfx : dfx['Word'].apply(list))\
                        .explode('Letter')\
                        .assign(letter_score = lambda dfx : dfx['Letter'].str.lower().map(map_dict))\
                        .groupby('Word', as_index=False)['letter_score'].sum()\
                        .rename(columns={'letter_score':'Score'})

# show(df_unique_words, df_poems)
df_output =   pd.merge(df_poems, df_unique_words, on='Word')\
                .assign(highest_score = lambda dfx : dfx.groupby('Poem')['Score'].transform('max'),
                        highest = lambda dfx : dfx['Score'] == dfx['highest_score'])
show(df_output)