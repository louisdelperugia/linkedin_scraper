from bs4 import BeautifulSoup
from src.div_till_section import parent_tag


def education(education_soup):
    '''
        Does:
            finds education section and gets info
        returns:
            education_list: which includes all educations that person has
    '''
    try:
        education_list=list()
        count=0
        tag_list=list()
        body=None
        desired_div=None

        # gets the body
        body=education_soup.body
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

        for li in lis:
            # tmp variables
            school_dict={'school':None,'department':None,'date':None,'grade':None,'summary':None}
            school_name=None
            department=None
            date=None
            grade=None
            activities=''
            summary=''

            # school
            for span in li.find_all('span',attrs={'class':"mr1 hoverable-link-text t-bold"}):
                # if there no section such it will return None
                if span.span!=None:
                    school_name=span.span.text
                    # adds to tmp school_dict
                    school_dict['school']=school_name
            # department or program
            for span in li.find_all('span',attrs={'class':"t-14 t-normal"}):
                # if there no section such it will return None
                if span.span!=None:
                    department=span.span.text
                    # adds to tmp school_dict
                    school_dict['department']=department
            # date
            for span in li.find_all('span',attrs={'class':"t-14 t-normal t-black--light"}):
                # if there no section such it will return None
                if span.span!=None:
                    date=span.span.text
                    # adds to tmp school_dict
                    school_dict['date']=date
            # summary
            for ul in li.find_all('ul',attrs={'class':"pvs-list"}):
                for li in ul.find_all('li',attrs={'class':""}):
                    # Grade
                    if '<!-- -->Grade:' in str(li):
                        # if there no section such it will return None
                        if li.span!=None:
                            grade=li.span.text
                            # will drop unnecesary part of the grade
                            grade=grade.replace('Grade: ','')
                            # adds to tmp school_dict
                            school_dict['grade']=grade
                    # activities
                    elif '<!-- -->Activities and societies:' in str(li):
                        # if there no section such it will return None
                        if li.span!=None:
                            activities=li.span.text
                    # summary
                    else:
                        # if there no section such it will return None
                        if li.span!=None:
                            summary=li.span.text
                    # combine activities and summary section
                    summary=(summary+' '+activities).strip()
                    # adds to tmp school_dict
                    if summary=='':
                        school_dict['summary']=None
                    else:
                        school_dict['summary']=summary
            # adds all tmp school_dict to main education_list
            education_list.append(school_dict)

        tmp_dict1={'school': None, 'department': None, 'date': None, 'grade': None, 'summary': None}
        # if there is no education , for some reason it adds tmp_dict1 dictionary to education, to prevent this:
        if len(education_list)==1 and tmp_dict1 in education_list:
            return []
        else:
            return education_list
    except:
        return []
