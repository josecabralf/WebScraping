from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup

def getSoup(link):
    options = ChromeOptions()
    options.add_argument("--headless=new")
    driver = Chrome(options=options)
    driver.get(link)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return soup