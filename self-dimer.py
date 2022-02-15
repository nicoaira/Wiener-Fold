from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import re
from datetime import datetime
import os
from multiprocessing import Pool
import sys
import os




def run_self_dimer(nrows, batches):

    print('Script #' + str(sys.argv[1]))


    batches_contador = 1

    driver = webdriver.Chrome()

    for i in range(50):
        try:
            driver.get("https://www.idtdna.com/site/account")
            print('Conexion exitosa en Script #' + str(sys.argv[1]) )
            break
        except:
            print('No se pudo acceder al sitio, intentandolo nuevamente...')


    try:

        driver.find_element(By.XPATH, '//*[@id="modal-holiday"]/div/div/div[3]/a').click()

        # WebDriverWait(driver, 20
        # ).until_not(EC.visibility_of_element_located(By.XPATH, '//*[@id="modal-holiday"]//*[@class="modal-content"]'))
        time.sleep(5)


    except:
        pass


    with open('login.txt') as f:
        lines = f.readlines()

    driver.find_element(By.ID, 'UserName').send_keys(lines[0])
    driver.find_element(By.ID, 'Password').send_keys(lines[1])
    driver.find_element(By.ID, 'Password').send_keys(Keys.ENTER)

    try:
        WebDriverWait(driver, 150
        ).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ProgressDialog"]/div')))
        WebDriverWait(driver, 150
        ).until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="ProgressDialog"]/div')))

    except TimeoutException:
        print("Timed out, la pagina no se pudo cargar")

    time.sleep(10)
    driver.get("https://www.idtdna.com/calc/analyzer")


    for batch in range(batches):

        print('Script #' + str(sys.argv[1]) + ' - Batch #'+str(batches_contador))

        start_batch = time.time()
        time.sleep((int(sys.argv[1]))*12)

        df = pd.read_csv('deltaG_sorted.csv')
        df_temp = df[:nrows]

        now = datetime.now()
        temp_name = 'deltaG_temp'
        temp_name +=  now.strftime('%d-%m-%Y-%H-%M-%S')
        temp_name += '.csv'

        found = False

        for n in range(15):

            print('n =', n, 'Script# ', str(sys.argv[1]))

            if found == True:
                break
            else:
                pass

            df_temp.to_csv(temp_name, index = False)

            files_names = os.listdir()

            for file_name in files_names:
                if temp_name in file_name:
                    found = True
                    print('Dafaframe de respaldo creado en Script #' + str(sys.argv[1]) )
                    break
                else:
                    pass


        # Elimina las filas del df y lo guarda
        df_drop = df.drop(range(nrows))
        df_drop.to_csv('deltaG_sorted.csv', index = False)


        sequences = []


        for i in range(nrows):

            start = time.time()

            nro_secuencia = ((batches_contador-1)*nrows)+i+1

            print('Script #' + str(sys.argv[1]) + ' - Secuencia #' + str(nro_secuencia))

            dict_temp = {
                'sequence' : df_temp.iloc[i]['sequence'],
                'hairpin_dG': df_temp.iloc[i]['dG'],
                'hairpin_num_structures' : df_temp.iloc[i]['num_structures'],
                'selfdimer_dG' : None,
                'min_selfdimer_dG' : None,
                'selfdimer_num_structures' : None,
                'tm': df_temp.iloc[i]['tm'],
                'triggerX_tm' : df_temp.iloc[i]['triggerX_tm'],
            }

            sequence = dict_temp['sequence']


            driver.find_element(By.ID, 'textarea-sequence').clear()

            driver.find_element(By.ID, 'textarea-sequence').send_keys(sequence)
            self_dimer = driver.find_element(By.XPATH, '//*[@id="rmenu"]/div/div[6]/button')
            driver.execute_script("arguments[0].click();", self_dimer)

            try:
                WebDriverWait(driver, 140
                ).until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="OAResults"]/span/img')))
                WebDriverWait(driver, 60
                ).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "kcal/mole")]')))
            except TimeoutException:
                print("Timed out, no se pudo cargar la secuencia", nro_secuencia)
                print('Secuencia salteada:', sequence)
                continue



            deltaG = driver.find_elements(By.XPATH, '//*[contains(text(), "kcal/mole")]')

            deltaG_num = []

            for j in deltaG[1:]:
                num = re.search(r"-?\d*\.*\d*", j.text).group()
                deltaG_num.append(float(num))

            dict_temp['selfdimer_dG'] = sum(deltaG_num)
            dict_temp['selfdimer_num_structures'] = len(deltaG_num)
            dict_temp['min_selfdimer_dG'] = min(deltaG_num)



            sequences.append(dict_temp)

            end = time.time()

            # print('Procesado en:', round(end-start, 2), 's')

        df_temp = pd.DataFrame(sequences)

        try:
            df = pd.read_csv('deltaG_final.csv')
        except:
            print('Creando dataframe...')
            columns = [
            'sequence',
            'hairpin_dG',
            'hairpin_num_structures',
            'selfdimer_dG',
            'min_selfdimer_dG',
            'selfdimer_num_structures',
            'tm',
            'triggerX_tm'
            ]

            df = pd.DataFrame(columns = columns)

        df = pd.concat([df, df_temp])

        df.to_csv('deltaG_final.csv', index = False)

        os.remove(temp_name)

        batches_contador += 1

        end_batch = time.time()

        print('Tiempo de batch=', round(end_batch-start_batch, 2), 's')

    print('Script# ' + str(sys.argv[1]) +' - Fin del analisis!')



run_self_dimer(nrows = int(sys.argv[2]), batches = int(sys.argv[3]))

# run_self_dimer(nrows = 50, batches = 3)
