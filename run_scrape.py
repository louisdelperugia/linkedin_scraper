import sys, os, time
import pandas as pd
from bs4 import BeautifulSoup

from connect import linkedin_connect, save_html
from src.div_till_section import div_till_section
from src.header import header
from src.about import about
from src.experience import experience

https://www.scraperapi.com/blog/linkedin-scraper-python/
def save_to_pkl(header_info, experience_info, url):

    df = pd.DataFrame(columns=['full_name', 'current_title', 'location', 'experience', 'url'])

    df.loc[0] = [header_info['full_name'], header_info['current_title'], header_info['location'],
                 experience_info, url]

    df_scraped = pd.read_pickle('data/scraped_profiles.pkl')
    print(df_scraped)
    if url not in list(df_scraped['url']):
        df_concatted = pd.concat([df_scraped, df], ignore_index=True)
        df_concatted.to_pickle('data/scraped_profiles.pkl', protocol=4)
    print(df.iloc[0])


def call_all_sections(url, driver):

    page_list = save_html(url, driver)
    driver = page_list[0]

    html_codes = page_list[1]
    html_codes_experience = page_list[4]


    soup = BeautifulSoup(html_codes, 'html.parser')
    experience_soup = BeautifulSoup(html_codes_experience, 'html.parser')

    body = soup.find_all('body')[0]
    desired_div = div_till_section(body)
    all_section = desired_div.find_all('section')

    header_section = None
    about_section = None
    people_also_viewed_section = None
    for section in all_section:
        if 'id="profile-sticky-header-toggle"' in str(section):
            header_section = section
        elif 'id="about"' in str(section):
            about_section = section

    header_info = header(header_section, all_section)

    experience_info = experience(experience_soup)
    save_to_pkl(header_info, experience_info, url)
    return driver

if __name__ == "__main__":
    driver = linkedin_connect()
    input_string = input('Type anything and click enter to continue: ')
    df_url = pd.read_csv('list.csv', header=None, names=['url'])
    count = 0
    for index, row in df_url.iterrows():
        url = row['url']
        print(url)
        driver = call_all_sections(url, driver)
        count += 1
        print(count)
    driver.quit()
