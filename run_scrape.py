# python libraries
import sys
import os
import time
import pandas as pd
from bs4 import BeautifulSoup

# path of folder "sections", change and enter your path below
sys.path.insert(0,'.../Desktop/linkedin_scraper/sections/')
# functions from different scripts
from connect import linkedin_connect,save_html
from div_till_section import div_till_section
from header import header
from about import about
from experience import experience
from skills import skills
from education import education
from certifications import certifications
from languages import languages

def save_to_pkl(header_info,summary_info,skills_info,education_info,experience_info,certifications_info,languages_info,url):
    '''
        Does:
            gets all info after profile is scraped, creates dataframe and saves it

        returns:
    '''
    # creates empty dataframe with column names
    df=pd.DataFrame(columns=['full_name','current_title','location','summary','skills','education','experience','certifications','languages','linkedin_url'])
    # adds info to the dataframe
    df.loc[0]=[header_info['full_name'],header_info['current_title'],header_info['location'],summary_info,skills_info,education_info,experience_info,certifications_info,languages_info,url]
    # read data
    df_scraped=pd.read_pickle('data/scraped_profiles.pkl')
    # if url already exist in the data, then it wont add new profile
    if url not in list(df_scraped['linkedin_url']):
        # concats 2 df
        df_concatted=pd.concat([df_scraped,df],ignore_index=True)
        # saves concatted data
        df_concatted.to_pickle('data/scraped_profiles.pkl',protocol=4)
    # shows scraped profile
    print(df.iloc[0])

def call_all_sections(url,driver):
    # # connects to linkedin via chromedriver
    # driver=linkedin_connect()

    # returns list which includes driver and html codes of each section
    page_list=save_html(url,driver)
    # index 0  is driver
    driver=page_list[0]

    # all indexes except 0 are html source codes
    # html_codes page html
    html_codes=page_list[1]
    # skills page html
    html_codes_skills=page_list[2]
    # educationpage html
    html_codes_education=page_list[3]
    # experience_page html
    html_codes_experience=page_list[4]
    # certifications_page html
    html_codes_certifications=page_list[5]
    # languages_page html
    html_codes_languages=page_list[6]


    # ----------PAGE SOURCES TO BeautifulSoup TYPE-------------
    # all page source
    soup=BeautifulSoup(html_codes,'html.parser')
    # skills page source
    skills_soup=BeautifulSoup(html_codes_skills,'html.parser')
    # education page source
    education_soup=BeautifulSoup(html_codes_education,'html.parser')
    # experience page source
    experience_soup=BeautifulSoup(html_codes_experience,'html.parser')
    # certifications page source
    certifications_soup=BeautifulSoup(html_codes_certifications,'html.parser')
    # languages page source
    languages_soup=BeautifulSoup(html_codes_languages,'html.parser')


    # just 1 body in html
    body=soup.find_all('body')[0]
    # desired div from body , div_till_section finds main div of the source
    desired_div=div_till_section(body)
    # gets all the sections from main html page
    all_section=desired_div.find_all('section')


    # some parts belong to main page, so by getting all_sections we can get them
    header_section=None
    about_section=None
    people_also_viewed_section=None
    for section in all_section:
        if 'id="profile-sticky-header-toggle"' in str(section):
            header_section=section
        elif 'id="about"' in str(section):
            about_section=section

    # gets info in different types
    # dict
    header_info=header(header_section,all_section)
    # str
    summary_info=about(about_section)
    # list
    skills_info=skills(skills_soup)
    # list->dict
    education_info=education(education_soup)
    # list->dict
    experience_info=experience(experience_soup)
    # list->dict
    certifications_info=certifications(certifications_soup)
    # list->dict
    languages_info=languages(languages_soup)

    save_to_pkl(header_info,summary_info,skills_info,education_info,experience_info,certifications_info,languages_info,url)

    return driver

def url_corrector(url):
    '''
        Does: fixes url to desired type (https://www.linkedin.com/in/slug/)
    '''
    # if no problem returns same url
    if url[:24]=='https://www.linkedin.com':
        return url
    else:
        # if there is a problem,  will url to desired format
        problematic_part=''
        for i in range(len(url)):
            if url[i]=='m' and url[i+1]=='/' and url[i+2]=='i' and url[i+3]=='n':
                problematic_part=url[:i+1]
                break
        url=url.replace(problematic_part,'https://www.linkedin.com')
        return url

if __name__ == "__main__":
    # connects to linkedin via chromedriver
    driver=linkedin_connect()
    input_string=input('Type anything and click enter to continue: ')
    # read data, enter your csv file's path
    df_url=pd.read_csv('...path_to_the_csv')
    # gets first 10 urls
    df_url=df_url.iloc[:10]
    count=0
    # linkedin url of the person
    for index,row in df_url.iterrows():
        url=row['linkedin_url']
        # if url is None
        if url==None:
            continue
        # if format of the url provlematic call this function
        url=url_corrector(url)
        # if las char is not '/' then adds it
        if url[-1]!='/':
            url=url+'/'
        try:
            driver=call_all_sections(url,driver)
        except Exception as e:
            print(e)
        count+=1
        print(count)
    # closes chromes web page
    driver.quit()
