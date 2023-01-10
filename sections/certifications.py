from bs4 import BeautifulSoup
from div_till_section import parent_tag

def certifications(certifications_soup):
    try:
        certifications_list=list()
        count=0
        tag_list=list()
        body=None
        desired_div=None

        # gets the body
        body=certifications_soup.body
        # gets all desired divs and finds desired one
        for div in body.find_all('div'):
            if 'id="main"' in str(div):
                tag_list.append(div)

        desired_div=parent_tag(tag_list)
        tag_list=list()

        section=desired_div.section

        # gets all desired divs and finds desired one
        for div in section.find_all('div'):
            if 'li class="pvs-list__paged-list-item' in str(div):
                tag_list.append(div)

        desired_div=parent_tag(tag_list)
        tag_list=list()

        ul=desired_div.ul

        # gets all desired lis
        lis=list()
        for li in ul.find_all('li'):
            if 'class="pvs-list__paged-list-item' in str(li):
                lis.append(li)

        # gets all as' as set
        a_set=set()
        for li in lis:
            for div in li.find_all('div'):
                if 'a class="optional-action-target-wrapper' and '<a class' in str(div):
                    for  a in div.find_all('a'):
                        if '<a class="optional-action-target-wrapper display-flex flex-column full-width"' in str(a):
                            a_set.add(a)
        # all a's in a_set
        for a in a_set:
            tmp_dict={'course':None,'company':None}
            for span in a.find_all('span'):
                if 'class="mr1 hoverable-link-text t-bold"' in str(span):
                    # school
                    tmp_dict['course']=span.span.text
                elif 'class="t-14 t-normal"' in str(span):
                    # department
                    tmp_dict['company']=span.span.text
            certifications_list.append(tmp_dict)


        return certifications_list
    except:
        return []
