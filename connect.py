import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import requests
import random

def chrome_driver():
    # path to the chromedriver,chane and enter your path below
    ser = Service("...linkedin_scraper/chromedriver")
    opt = webdriver.ChromeOptions()
    # # opens chrome driver but wont show chrome pages
    #opt.add_argument("headless")
    # enables automation
    opt.add_experimental_option("useAutomationExtension", False)
    opt.add_experimental_option("excludeSwitches",["enable-automation"])
    driver = webdriver.Chrome(service=ser, options=opt)
    return driver

def linkedin_connect():
    driver=chrome_driver()

    driver.get('https://www.linkedin.com/login')

    # enter your mail and password to login linkedin
    email = ""
    passw = ""

    # locate email form by_class_name
    username = driver.find_element_by_id('username')
    # send_keys() to simulate key strokes
    username.send_keys(email)
    # locate password form by_class_name
    password = driver.find_element_by_id('password')
    # send_keys() to simulate key strokes
    password.send_keys(passw)
    time.sleep(0.5)
    # locate submit button by_class_name
    log_in_button = driver.find_element_by_class_name('login__form_action_container ')
    # .click() to mimic button click
    log_in_button.click()

    return driver

def save_html(url,driver):
    # scrapes main page's html codes
    driver.get(url)
    time.sleep(random.randint(3, 5))
    all_page=driver.page_source

    # scrapes skills page's html codes
    driver.get(f'{url}details/skills/')
    time.sleep(random.randint(6, 8))
    skills_page=driver.page_source

    # scrapes education page's html codes
    driver.get(f'{url}details/education/')
    time.sleep(random.randint(5, 7))
    education_page=driver.page_source

    # scrapes experience page's html codes
    driver.get(f'{url}details/experience/')
    time.sleep(random.randint(10, 12))
    experience_page=driver.page_source

    # scrapes certification page's html codes
    driver.get(f'{url}details/certifications/')
    time.sleep(random.randint(5, 7))
    certifications_page=driver.page_source

    # scrapes language page's html codes
    driver.get(f'{url}details/languages/')
    time.sleep(random.randint(2, 4))
    languages_page=driver.page_source

    return [driver,all_page,skills_page,education_page,experience_page,certifications_page,languages_page]

if __name__ == "__main__":
    driver=linkedin_connect()
    input_string=input('Type anything and click enter to continue: ')
    url='https://www.linkedin.com/in/williamhgates/'
    page_list=save_html(url,driver)
    driver=page_list[0]
    driver.quit()
