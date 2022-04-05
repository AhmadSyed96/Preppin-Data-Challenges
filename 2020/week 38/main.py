import pandas as pd

def anagram(row):
    row['anagram'] = sorted(row['Word 1'].lower()) == sorted(row['Word 2'].lower())
    return row
df = pd.read_excel('Input - Anagrams (1).xlsx', sheet_name='Anagrams').apply(anagram, axis=1)
print(df)