import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

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
                   seleniumwire_options=proxy_options)

driver.execute_cdp_cmd('Storage.clearDataForOrigin',
                       {"origin": '*', "storageTypes": 'all', })

df_url = pd.read_csv('linkedin_url.csv')

for i in range(len(df_url)):
    url = df_url.iloc[i,1]
    driver.get(url)
    time.sleep(10)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="public_profile_contextual-sign-in"]/div/section/button/icon'))).click()
    time.sleep(10)

eee





