import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

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

url ="https://www.linkedin.com/in/maria-meinero-930b46173"
driver.get(url)
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="public_profile_contextual-sign-in"]/div/section/button/icon'))).click()
WebDriverWait(driver, 20)


exp_desc = driver.find_element(by=By.XPATH, value = '//*[@id="main-content"]/section[1]/div/section/section[3]/div/ul')
soup = BeautifulSoup(exp_desc.get_attribute('outerHTML'),'html.parser')
soup = str(soup)
appended_data = []

soup = BeautifulSoup(soup, "html.parser")
content = soup.find_all('li')
content_list = []

for ele in content:
    sub_title = ele.find('h3').text
    row = [sub_title]
    h4 = ele.find('h4').text
    row.append(h4)
    href = ele.find('h4').find('a', href=True)['href']
    row.append(href)
    time = ele.find('div').find('p')
    row.append(time)
    content_list.append(row)

print('aaaaaaa')

appended_data = pd.DataFrame(content_list)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_seq_items', 500000)

print(appended_data)
