from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

##TODO dockerizar o projeto e instalar o chrome driver na instacia 
## antes será necessário rodar o projeto localmente sem venv para a busca no  chrome funcionar!!!!

def web_search(fullname) -> str:
  
    driver = webdriver.Chrome()

    driver.get('https://www.gov.br/imprensanacional/pt-br')

    driver.implicitly_wait(15)
    try:

        close_pop_up = driver.find_element(By.TAG, 'body')
        close_pop_up.click()
        
        # Seleciona o iframe do buscador
        iframe = driver.find_element(By.ID, 'buscadou-iframe')
        driver.switch_to.frame(iframe)
    
        
        search_bar = driver.find_element(By.XPATH, '//*[@id="search-bar"]') 
        search_bar.send_keys(fullname)
        search_bar.submit()

    except Exception as e:
        print(e)
    
    finally:
        driver.quit()
