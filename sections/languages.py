from bs4 import BeautifulSoup
from div_till_section import parent_tag


def languages(languages_soup):
    '''
        Does:
            gets language section and scrapes info from it
        returns:
            language_list: which contains language info
    '''
    try:
        # will contain language info
        language_list=list()
        # gets main section
        for main in languages_soup.find_all('main',attrs={"id":"main"}):
            desired_main=main

        # gets language and its level
        for div in desired_main.find_all('div',attrs={"class":"display-flex flex-column full-width"}):
            tmp_language_dict={'language':None,'level':None}
            language=None
            level=None
            # language
            for span in div.find_all('span',attrs={"class":"mr1 t-bold"}):
                if span.span!=None:
                    language=span.span.text
            # level
            for span in div.find_all('span',attrs={"class":"t-14 t-normal t-black--light"}):
                if span.span!=None:
                    level=span.span.text
            # adds language to tmp dictionary
            tmp_language_dict['language']=language
            # adds language level to tmp dictionary
            tmp_language_dict['level']=level

            # adds tmp dictionary to main language_list
            language_list.append(tmp_language_dict)


        return language_list
    except:
        return []
