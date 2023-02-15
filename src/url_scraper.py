from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
from selenium.webdriver.common.by import By

st = input("Enter keywords you want to search- ")
search_string = str(st.replace(' ', '+'))



ser = Service("...linkedin_scraper/chromedriver")
opt = webdriver.ChromeOptions()
opt.add_argument("--incognito")
opt.add_experimental_option("useAutomationExtension", False)
opt.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(service=ser, options=opt)

driver.execute_cdp_cmd('Storage.clearDataForOrigin', {
    "origin": '*',
    "storageTypes": 'all',
})

driver.get("https://www.google.com/search?q=" + search_string + "&start=" + str('1'))

max_page = 2
all_urls = []
page = 1
while True:
    time.sleep(20)

    urls = driver.find_elements(by=By.CLASS_NAME, value='yuRUbf')
    urls = [url.find_element(by=By.TAG_NAME, value='a') for url in urls]
    urls = [url.get_attribute("href") for url in urls]
    all_urls = all_urls + urls


    page += 1

    if page > max_page:
        print('\n end at page:' + str(page - 1))
        break

    try:
        next_page = driver.find_element(By.ID, value='pnnext')
        next_page.click()
    except:
        print('\n end at page:' + str(page - 1) + ' (last page)')
        break

df = pd.DataFrame(all_urls)
df.to_csv('linkedin_url.csv')