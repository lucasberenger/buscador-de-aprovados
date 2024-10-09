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

    # driver.implicitly_wait(15)
    try:
        print("Esperando pop_up...")

        wait_pop_up = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="govbr-login-overlay-wrapper"]'))
        )

        print("Popup encontrado")
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="govbr-login-overlay-wrapper"]'))
        )

        close_pop_up = driver.find_element('xpath', '//*[@id="govbr-login-overlay-wrapper"]')
        close_pop_up.click()
        print("pop_up fechado!")
        
        search_box = driver.find_element('xpath', '//*[@id="search-bar"]') 
        search_box.send_keys(fullname)
        search_box.submit()

    except Exception as e:
        print(e)
    
    finally:
        driver.quit()


# close_login = driver.find_element(By.ID, 'govbr-login-overlay-wrapper')
    # close_login = driver.find_element('xpath', '//*[@id="sso-status-bar"]/div[2]/div[1]')
    # close_login.click()

    # search_box = driver.find_element('xpath', '//*[@id="search-bar"]') 
    # search_box.send_keys(fullname)
    # search_box.submit()