from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

##TODO dockerizar o projeto e instalar o chrome driver na instacia 
## antes será necessário rodar o projeto localmente sem venv para a busca no  chrome funcionar!!!!

def web_search(fullname) -> str:

    service = ChromeDriverManager().install()

    driver = webdriver.Chrome(service=service)

    driver.get('https://www.gov.br/imprensanacional/pt-br')

    driver.implicity_wait(10)

    search_box = driver.find_element('xpath', '//*[@id="search-bar"]') 
    search_box.send_keys(fullname)
    search_box.submit()

    driver.quit()

