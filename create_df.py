import pandas as pd


columns = ['sequence','num_structures','dG', 'tm', 'triggerX_tm']
df = pd.DataFrame(columns = columns)

df.to_csv('deltaG.csv', index = False)
