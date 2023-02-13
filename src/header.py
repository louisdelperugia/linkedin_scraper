from bs4 import BeautifulSoup
from src.div_till_section import parent_tag


def header(header_section,all_section):
    '''
        Does:
            scrapes main page and gets full_name, current_title, location
        returns:
            {'full_name':name,'current_title':title,'location':location}
    '''
    try:
        full_name=None
        current_title=None
        location=None
        header_dict={'full_name':None,'current_title':None,'location':None}
        desired_div=''

        # Header gets ph5 ph5 class div
        for div in header_section.find_all('div',attrs={"class":"ph5 pb5"}):
            for div1 in div.find_all('div',attrs={"class":"mt2 relative"}):
                desired_div=div1
        # the class is note ph5 ph5 then gets "class":"ph5"
        if desired_div=='':
            for div in header_section.find_all('div',attrs={"class":"ph5"}):
                for div1 in div.find_all('div',attrs={"class":"mt2 relative"}):
                    desired_div=div1

        # name and current_title
        for div in desired_div.find_all('div',attrs={"class":"pv-text-details__left-panel reduced-spacing"}):
            # name
            for h1 in div.find_all('h1'):
                full_name=h1.text
                header_dict['full_name']=full_name
            # current_title
            for div1 in div.find_all('div',attrs={"class":"text-body-medium break-words"}):
                current_title=div1.text.strip()
                header_dict['current_title']=current_title
        # location
        for span in desired_div.find_all('span',attrs={"class":"text-body-small inline t-black--light break-words"}):
            location=span.text.strip()
            header_dict['location']=location

        return header_dict
    except:
        return {'full_name':None,'current_title':None,'location':None}
