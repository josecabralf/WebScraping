from selenium import webdriver
from config import *
from scraperZonaProp import scrapZonaProp

driver = webdriver.Chrome(path_driver)
driver.get(URL_ZonaProp)

paginas = True

while paginas:
    try:
        nro_pagina = (driver.find_element_by_xpath(
            '//a[@class = "sc-n5babu-1 llkTcd"]')).text
        scrapZonaProp(driver, f"{archivos_ZonaProp}pagina{nro_pagina}.json")

    except:
        paginas = False

driver.quit()
