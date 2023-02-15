import random, time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By



def chrome_driver():
    ser = Service("...linkedin_scraper/chromedriver")
    opt = webdriver.ChromeOptions()
    opt.add_experimental_option("useAutomationExtension", False)
    opt.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(service=ser, options=opt)

    driver.execute_cdp_cmd('Storage.clearDataForOrigin', {
        "origin": '*',
        "storageTypes": 'all',
    })
    return driver
ss

def linkedin_connect():
    driver = chrome_driver()

    driver.get('https://www.linkedin.com/login')

    email = "morriz.fillip@outlook.com"
    passw = "WmMLc6VYNunFD8X"

    username = driver.find_element(by=By.ID, value='username')
    username.send_keys(email)
    time.sleep(random.randint(1, 4))
    password = driver.find_element(by=By.ID, value='password')
    password.send_keys(passw)
    time.sleep(random.randint(1, 4))
    log_in_button = driver.find_element(by=By.CLASS_NAME, value='login__form_action_container ')
    log_in_button.click()
    return driver


def save_html(url, driver):
    driver.get(url)
    time.sleep(random.randint(3, 5))
    all_page = driver.page_source
    driver.get(f'{url}details/experience/')
    time.sleep(random.randint(10, 12))
    experience_page = driver.page_source

    return [driver, all_page, experience_page]