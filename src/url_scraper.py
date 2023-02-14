from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By

def create_search_url(title, location, *include):
    result = ""
    base_url = "http://www.google.com/search?q=+-intitle:%22profiles%22+site:linkedin.com/in/+OR+site:linkedin.com/pub/"

    quote = lambda x: "%22" + x + "%22"

    result += base_url
    result += quote(title) + "+" + quote(location)

    for word in include:
        result += "+" + quote(word)
    return result

max_page = 2
all_urls = []

ser = Service("...linkedin_scraper/chromedriver")
opt = webdriver.ChromeOptions()
opt.add_experimental_option("useAutomationExtension", False)
opt.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(service=ser, options=opt)

driver.execute_cdp_cmd('Storage.clearDataForOrigin', {
    "origin": '*',
    "storageTypes": 'all',
})

# always start from page 1
page = 1

driver.get(create_search_url("software engineer", "european commission", "developer"))

while True:
    time.sleep(20)

    # find the urls
    urls = driver.find_element(by=By.CLASS_NAME, value='r')
    urls = [url.find_element(by=By.TAG_NAME, value='a') for url in urls]
    urls = [url.get_attribute("href") for url in urls]
    all_urls = all_urls + urls

    # move to the next page
    page += 1

    if page > max_page:
        print('\n end at page:' + str(page - 1))
        break

    try:
        next_page = driver.find_element(by=By.CSS_SELECTOR, value="a[aria-label='Page " + str(page) + "']")
        next_page.click()
    except:
        print('\n end at page:' + str(page - 1) + ' (last page)')
        break

print(all_urls)