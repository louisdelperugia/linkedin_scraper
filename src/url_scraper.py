import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

st = input("Enter keywords you want to search- ")
search_string = str(st.replace(' ', '+'))

API_KEY = '9bcf40e14bb4e30ded56421f15645949'

proxy_options = {
    'proxy': {
        'http': f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001',
        'no_proxy': 'localhost,127.0.0.1'
    }
}

opt = uc.ChromeOptions()
opt.add_argument("--incognito")
opt.add_argument('--no-sandbox')
opt.add_argument('--disable-dev-sh-usage')

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}

driver = uc.Chrome(options=opt,
                            desired_capabilities=caps,
                   seleniumwire_options = proxy_options
)

driver.execute_cdp_cmd('Storage.clearDataForOrigin', {
    "origin": '*',
    "storageTypes": 'all',
})

driver.get(
    "https://www.google.com/search?q=" +
    "site:www.linkedin.com/in " +
    search_string +
    "&start=" +
    str('1'))

max_page = 5
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
print(df.head())
df.to_csv('linkedin_url.csv')

