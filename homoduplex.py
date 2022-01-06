from seqgenerator import EXPAR
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import re


seq_list = []
driver = webdriver.Chrome()

driver.get("https://www.idtdna.com/site/account")
driver.find_element(By.ID, 'UserName').send_keys('wiener.fold')
driver.find_element(By.ID, 'Password').send_keys('wiener2022')
driver.find_element(By.ID, 'Password').send_keys(Keys.ENTER)
time.sleep(8)
driver.get("https://www.idtdna.com/calc/analyzer")
driver.find_element(By.ID, 'textarea-sequence').clear()

sequence = 'ACGTACGTACGTACGTACGTACGTACGTACGT'

driver.find_element(By.ID, 'textarea-sequence').send_keys(sequence)
self_dimer = driver.find_element(By.XPATH, '//*[@id="rmenu"]/div/div[6]/button')
driver.execute_script("arguments[0].click();", self_dimer)
time.sleep(4)

prueba  = driver.find_element(By.XPATH, '//*[@id="OAResults"]')

# resultados = driver.find_element(By.XPATH, '//*[@id="OAResults"]')
print(prueba.text)
print(prueba.text.find("5' "))


# driver.find_element(By.ID, 'temp').clear()
# driver.find_element(By.ID, 'temp').send_keys('55')
# driver.find_element(By.ID, 'Sodium').clear()
# driver.find_element(By.ID, 'Sodium').send_keys('0.05')
# driver.find_element(By.ID, 'Magnesium').clear()
# driver.find_element(By.ID, 'p').clear()
# driver.find_element(By.ID, 'p').send_keys('50')u
