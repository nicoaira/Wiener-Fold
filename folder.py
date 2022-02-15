from seqgenerator import EXPAR
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re


for i in range(40):

    seq_list = []
    driver = webdriver.Chrome()

    for j in range(30):

        secuencias = []

        for k in range (50):
            seq, seq_tm, templateX, templateX_tm = EXPAR(14, .41)

            sec_temp = {
            'indice': k+1,
            'sequence': templateX,
            'num_structures': None,
            'dG': None,
            'tm': templateX_tm,
            'triggerX_tm' : seq_tm
             }


            secuencias.append(sec_temp)

            secuencias_string = ''


        for sec_dict in secuencias:

            templateX = sec_dict['sequence']
            secuencias_string += templateX + '; '



        driver.get("http://www.unafold.org/Dinamelt/applications/quickfold.php")
        driver.find_element(By.ID, 'name').send_keys('Wiener-Fold')
        driver.find_element(By.ID, 'seq').send_keys(secuencias_string)
        driver.find_element(By.ID, 'temp').clear()
        driver.find_element(By.ID, 'temp').send_keys('55')
        driver.find_element(By.ID, 'Sodium').clear()
        driver.find_element(By.ID, 'Sodium').send_keys('0.05')
        driver.find_element(By.ID, 'Magnesium').clear()
        driver.find_element(By.ID, 'Magnesium').send_keys('0.007273')
        driver.find_element(By.ID, 'p').clear()
        driver.find_element(By.ID, 'p').send_keys('50')

        driver.find_element(By.XPATH, '//input[@type = "submit"]').click()


        time.sleep(5)

        # try:

        # Busca los nombres de las seucencias (secuencia 1, secencias 2, ...)
        list_seq = driver.find_elements(By.XPATH, '//*[contains(text(), "Sequence ")]')

        # Nos quedamos con el texto de los elementos encontrados
        list_seq_strings = []
        for seq in list_seq:
            seq = re.search(r"\d+", seq.text).group()
            list_seq_strings.append(seq)

        list_seq = list_seq_strings

        # Contamos la cantidad de estrucutras encontradas para cada secuencia
        # Se forma un diccionario con key secuencia # y como valor la cantidad
        # de esctructuras
        contador_seq = {i:list_seq.count(i) for i in list_seq}

        # Busca los nombres de los deltaG de las secuencias
        list_dg = driver.find_elements(By.XPATH, '//*[contains(text(), "ΔG = ")]')

        list_dg_floats = []

        # Extrae los valores numericos del texto (el valor de deltaG y
        # los pasa a float)

        for dg in list_dg:
            dg = re.search(r"[-+]?\d*\.*\d*", dg.text).group()
            list_dg_floats.append(float(dg))


        # Generamos un diccionario donde las keys van a ser los nombres de las
        # secuencias. Lo inicializamos con valores 0.

        seq_dg = dict.fromkeys(list_seq, 0)

        # Recorremos la lista de seuencias y con el indice vamos extrayendo en
        # orden los valores de deltaG de la lista correspondiente.
        # Se van sumando todos los que correspondan a la misma secuencia.

        for index, seq in enumerate(list_seq):

            dg_temp = list_dg_floats[index]
            seq_dg[seq] += dg_temp

        print(seq_dg)


        for secuencia in secuencias:
            k = secuencia['indice']
            secuencia['dG'] = seq_dg[str(k)]
            secuencia['num_structures'] = contador_seq[str(k)]
            del secuencia['indice']

        print(secuencias)

        # except:
        #     print('error')
        #     continue


        df_temp = pd.DataFrame(secuencias)

        df = pd.read_csv('deltaG_14.csv')

        df = pd.concat([df, df_temp])

        df.to_csv('deltaG_14.csv', index = False)
