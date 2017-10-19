from selenium                          import webdriver
from pyvirtualdisplay                  import Display
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by      import By
from selenium.webdriver.support.ui     import WebDriverWait as wait
from selenium.webdriver.support        import expected_conditions as EC


import time
import json

KEY = "xxxxxx"
USERNAME = "xxxxx"

'''
    It creates a virtual display for not render,
    the display in the server because it may have problems.
'''
'''
display = Display(visible=0, size=(2000,2000))
display.start() #it will not open the navigatior
'''
'''
    Change the default size of Chrome Display
'''
chrome_options = Options()
chrome_options.add_argument("--window-size=1900,800")

#Start Driver
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get("http://www.bilbao.eus/opendata/es/inicio")

time.sleep(1)

#LogIn
#key = driver.find_element_by_id("lineaabierta-pin")
#key.send_keys(KEY)

#key = driver.find_element_by_id("lineaabierta-login")
#key.send_keys(USERNAME)

#entrar = driver.find_element(By.XPATH, '//*[@id="header"]/div[2]/div/div/div[3]/div[3]/div[2]/form/div[3]/input')
#entrar.click()

#Enter to catalog
entrer = driver.find_element(By.XPATH, '//*[@id="nav"]//li[2]//a')
entrer.click()

#Get all the list of datasets
title_list = driver.find_elements(By.XPATH, '//*[@class="rlist_tit"]')
next_page = 
#Enter to tab 'Cuentas'

'''
driver.switch_to_frame("Inferior")
driver.switch_to_frame("Niveles")
entrar = driver.find_element(By.XPATH, '//*[@id="pestanya2"]/a')
entrar.click()

#Enter to 'Cuenta'
driver.switch_to_default_content()
driver.switch_to_frame("Inferior")
driver.switch_to_frame("Cos")
entrar = driver.find_element(By.XPATH, '//*[@id="data_1"]/td[1]/a')
entrar.click()
'''

#Scrap all movements

driver.switch_to_default_content()


driver.switch_to_frame("Inferior")
driver.switch_to_frame("Cos")
passar = driver.find_element(By.XPATH, '//*[contains(@class, "next_acumulativo_")]')
passar1 = passar.get_attribute('class')
if passar1 == 'next_acumulativo_off ':
    pass
else:
    while passar:
        passar.click()
        driver.switch_to_default_content()
        driver.switch_to_frame("Inferior")
        driver.switch_to_frame("Cos")
        time.sleep(1) #No magrada...
        passar = driver.find_element(By.XPATH, '//*[contains(@class, "next_acumulativo_")]')
        passar1 = passar.get_attribute('class')
        if passar1 == 'next_acumulativo_off ':
            break

transaccions_format = {}
transaccions = []


conceptes1 = driver.find_elements(By.XPATH, '//*[@id="TablaBean02"]/tbody//th[@scope="row"]//a')
conceptes2 = driver.find_elements(By.XPATH, '//td[contains(@id, "FECHA")]')
conceptes3 = driver.find_elements(By.XPATH, '//*[@id="TablaBean02"]/tbody//tr//td[@class="tamanyomaximocolumna ltxt "]')
conceptes4 = driver.find_elements(By.XPATH, '//td[contains(@id, "DATA_VALOR")]')
conceptes5 = driver.find_elements(By.XPATH, '//*[contains(@id, "TablaBean02")]/td[6]')
conceptes6 = driver.find_elements(By.XPATH, '//*[contains(@id, "TablaBean02")]/td[5]')


i = 0
with open('data.json', 'w+') as f:
    while i<len(conceptes1):
        transaccions_format['Concepto']     = conceptes1[i].text
        transaccions_format['Fecha']        = conceptes2[i].text
        transaccions_format['Fecha Valor']  = conceptes4[i].text
        transaccions_format['Mas Datos']    = conceptes3[i].text
        transaccions_format['Importe']      = conceptes6[i].text
        transaccions_format['Saldo']        = conceptes5[i].text
        json.dump(transaccions_format.copy(), f)
        f.write('\n')
        i += 1