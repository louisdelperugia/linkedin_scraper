from bs4 import BeautifulSoup
from div_till_section import parent_tag

def skills(skills_soup):
    try:
        skills=list()
        count=0
        tag_list=list()
        body=None
        desired_div=None

        body=skills_soup.body
        for div in body.find_all('div'):
            if 'id="main"' in str(div):
                tag_list.append(div)

        desired_div=parent_tag(tag_list)
        tag_list=list()

        section=desired_div.section
        # divs till ul
        for div in section.find_all('div'):
            if 'class="artdeco-tabpanel active ember-view"' in str(div):
                tag_list.append(div)

        desired_div=parent_tag(tag_list)
        tag_list=list()
        #all uls
        uls=desired_div.ul

        for li in uls.find_all('li'):
            for span in li.find_all('span'):
                if span.span!=None:
                    skill=span.span.text.strip()
                    if skill!='':
                        skills.append(skill)

        return skills
    except:
        return []
