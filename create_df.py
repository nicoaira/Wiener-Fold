import pandas as pd


columns = ['Sequence','num_structures','dG', 'tm', 'TriggerX_tm']
df = pd.DataFrame(columns = columns)

df.to_csv('deltaG.csv', index = False)
