import pandas as pd
import os
import re



files_names = os.listdir()

backups = []

for file_name in files_names:
    if 'deltaG_temp' in file_name:
        backups.append(file_name)
        print(file_name)
    else:
        pass

if len(backups) > 0:
    df = pd.read_csv('deltaG_sorted.csv')

    for file in backups:
        df_temp = pd.read_csv(file)
        df = pd.concat([df, df_temp])

    df = df.sort_values(by=['num_structures','dG'], ascending = [True, False])
    df.to_csv('deltaG_sorted.csv', index = False)

    print('Dataframe guardado con exito!')

    for file in backups:
        os.remove(file)
        print('Se borro el archivo', file)

else:
    print('No hay datos para restaurar!')
