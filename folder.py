from seqgenerator import EXPAR
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import re


for i in range(3):

    seq_list = []
    driver = webdriver.Chrome()

    for i in range(30):
        seq, seq_tm, templateX, templateX_tm = EXPAR()
        driver.get("http://www.unafold.org/Dinamelt/applications/quickfold.php")
        driver.find_element(By.ID, 'name').send_keys('Wiener-Fold')
        driver.find_element(By.ID, 'seq').send_keys(templateX)
        driver.find_element(By.ID, 'temp').clear()
        driver.find_element(By.ID, 'temp').send_keys('55')
        driver.find_element(By.XPATH, '//input[@type = "submit"]').click()


        time.sleep(5)

        try:
            list_dg = driver.find_elements(By.XPATH, '//*[contains(text(), "ΔG = ")]')

            dg = 0
            for i in list_dg:
                i = re.search(r"[-+]?\d*\.\d+|\d+", i.text).group() #Extre el numero
                i = float(i) # pasa a float
                dg += i

            seq_list.append({
            'Sequence': templateX,
            'num_structures': len(list_dg),
            'dG': dg,
            'tm': templateX_tm,
            'TriggerX_tm' : seq_tm
             })

        except:
            continue


    df_temp = pd.DataFrame(seq_list)

    df = pd.read_csv('deltaG.csv')

    df = pd.concat([df, df_temp])

    df.to_csv('deltaG.csv', index = False)
