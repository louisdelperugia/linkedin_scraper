from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import pandas as pd
from selenium.webdriver.common.by import By


import undetected_chromedriver as uc
driver = uc.Chrome()
driver.get("https://nowsecure.nl")

ser = Service("...linkedin_scraper/chromedriver")
opt = webdriver.ChromeOptions()
opt.add_argument("--incognito")
opt.add_argument('--no-sandbox')
opt.add_argument('--disable-dev-sh-usage')
opt.add_experimental_option("useAutomationExtension", False)
opt.add_experimental_option("excludeSwitches", ["enable-automation"])

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}

driver = webdriver.Chrome(service=ser, options=opt,
                            desired_capabilities=caps)

driver.execute_cdp_cmd('Storage.clearDataForOrigin', {
    "origin": '*',
    "storageTypes": 'all',
})
url ="https://be.linkedin.com/in/escalantejuan"
print(url)
driver.get(url)
time.sleep(20)
ggg
next_page = driver.find_element(By.LINK_TEXT, 'Dismiss')
next_page.click()

bbbb
urls = driver.find_elements(by=By.CLASS_NAME, value='yuRUbf')

urls = [url.find_element(by=By.TAG_NAME, value='a') for url in urls]
urls = [url.get_attribute("href") for url in urls]
all_urls = all_urls + urls


df = pd.DataFrame(all_urls)
print(df.head())
df.to_csv('linkedin_url.csv')

