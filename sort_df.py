import pandas as pd
import os



print(os.listdir()[0])

df = pd.read_csv('deltaG.csv')
positive_dG = df['dG'] >= 0
df = df[positive_dG]
df = df.sort_values(by=['num_structures','dG'], ascending = [True, False])




df.to_csv('deltaG_sorted.csv', index = False)
