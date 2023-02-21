from bs4 import BeautifulSoup
import re

def personal_description(driver):
    pers_desc = driver.find_element(by=By.XPATH,
                                    value='//*[@id="main-content"]/section[1]/div/section/section[1]/div/div[2]/div[1]')
    soup = BeautifulSoup(pers_desc.get_attribute('outerHTML'), 'html.parser')
    soup = str(soup)
    content_list = []
    soup = BeautifulSoup(soup, "html.parser")

    name = soup.find('h1').text
    content_list.append(str.strip(name))
    region = soup.find_all('h3')
    for x in range(len(region)):
        content_list.append(str(re.sub(r'[^a-zA-Z0-9]', ' ', region[x].text)))
    return content_list

def experiences(driver):
    try:
        exp_desc = driver.find_element(by=By.CLASS_NAME,
                                       value='experience__list')
        soup = BeautifulSoup(exp_desc.get_attribute('outerHTML'), 'html.parser')
        soup = str(soup)
        experiences_list = []
        soup = BeautifulSoup(soup, "html.parser")
        content = soup.find_all('li')
        for ele in content:
            exp = []
            sub_title = ele.find('h3').text
            exp.append(str.strip(sub_title))
            h4 = ele.find('h4').text
            exp.append(str.strip(h4))
            time = ele.find('div').find('p')
            exp.append(str.strip(time.text))
            experiences_list.append(exp)
    except:
        experiences_list = None
    return experiences_list

def education(driver):
    try:
        educ_list = []
        education_desc = driver.find_element(by=By.CLASS_NAME,
                                             value='education__list')
        soup = BeautifulSoup(education_desc.get_attribute('outerHTML'), 'html.parser')
        soup = str(soup)
        soup = BeautifulSoup(soup, "html.parser")
        content = soup.find_all('li')

        for ele in content:
            exp = []
            sub_title = ele.find('h3').text
            exp.append(str.strip(sub_title))
            h4 = ele.find('h4').text
            exp.append(str.strip(h4))
            time = ele.find('div').find('p')
            exp.append(str.strip(time.text))
            educ_list.append(exp)
    except:
        educ_list = None
    return educ_list

