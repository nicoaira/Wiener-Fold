from seqgenerator import EXPAR
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import re


nrows = 50
batches = 1

batches_contador = 1

driver = webdriver.Chrome()

for i in range(3000):
    try:
        driver.get("https://www.idtdna.com/site/account")
        # element_present = EC.title_contains('Integrated')
        # WebDriverWait(driver, 1).until(element_present)
        break
    except:
        print('No se pudo acceder al sitio, intentandolo nuevamente...')

print('Conexion exitosa!')
driver.find_element(By.ID, 'UserName').send_keys('wiener.fold')
driver.find_element(By.ID, 'Password').send_keys('wiener2022')
driver.find_element(By.ID, 'Password').send_keys(Keys.ENTER)

try:
    element_present = EC.presence_of_element_located((By.ID, 'user-logged-in-controls'))
    WebDriverWait(driver, 30).until(element_present)

except TimeoutException:
    print("Timed out, la pagina no se pudo cargar")

driver.get("https://www.idtdna.com/calc/analyzer")


for batch in range(batches):

    print('Batch #'+str(batches_contador))

    start = time.time()

    df = pd.read_csv('deltaG_sorted.csv')

    df_temp = df[:nrows]

    sequences = []


    for i in range(nrows):

        nro_secuencia = ((batches_contador-1)*50)+i+1

        print('Secuencia #' + str(nro_secuencia))

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
        # time.sleep(2)

        if nro_secuencia == 1:
            time.sleep(4)
        else:
            try:
                WebDriverWait(driver, 15
                ).until_not(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Loading...")]')))
            except TimeoutException:
                print("Timed out, no se pudo cargar la secuencia", nro_secuencia)
                print('Secuencia salteada:', sequence)
                continue

        try:
            WebDriverWait(driver, 15
            ).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "kcal/mole")]')))
        except TimeoutException:
            print("Timed out, no se pudo cargar la secuencia", nro_secuencia)
            print('Secuencia salteada:', sequence)
            continue




        deltaG = driver.find_elements(By.XPATH, '//*[contains(text(), "kcal/mole")]')

        deltaG_num = []

        for j in deltaG[1:]:
            num = re.search(r"[-+]?\d*\.\d+|\d+", j.text).group()
            deltaG_num.append(float(num))

        dict_temp['selfdimer_dG'] = sum(deltaG_num)
        dict_temp['selfdimer_num_structures'] = len(deltaG_num)
        dict_temp['min_selfdimer_dG'] = min(deltaG_num)



        sequences.append(dict_temp)

    df_temp = pd.DataFrame(sequences)

    df = df.drop(range(nrows))
    df.to_csv('deltaG_sorted.csv', index = False)

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

    batches_contador += 1

    end = time.time()

    print('Tiempo de batch=', end-start)
