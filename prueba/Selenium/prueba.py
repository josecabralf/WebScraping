from selenium import webdriver

url = 'https://www.zonaprop.com.ar/inmuebles-venta-cordoba.html'
path_driver = '../../ZonaProp/driver/chromedriver'
URL_Base = 'https://www.zonaprop.com.ar'
driver = webdriver.Chrome(path_driver)
driver.get(url)

pagina_siguiente = driver.find_element_by_xpath(
    '//a[@data-qa = "PAGING_NEXT"]')
pagina_siguiente.click()
