from bs4 import BeautifulSoup

def not_nested_experience(lis):
    '''
        Does:
            finds not nested experience from html codes and will work on it , to save data
        returns:
            tmp_not_nested_exp_list: list which includes all not experience
    '''
    # all not nested experiences will be in this list
    tmp_not_nested_exp_list=list()
    for li in lis:
        #tmp dict
        tmp_exp_dict={'company':None,'title':None,'date':None,'summary':None,'skills':None}
        # case where experience is nested
        if ('class="scaffold-finite-scroll__content"' and 'class="mr1 hoverable-link-text t-bold"') not in str(li):
            # 4 tmp lists
            title_list=list()
            company_list=list()
            date_list=list()
            summary_list=list()
            skills_list=list()
            # all spans will be returned in this loop
            for span in li.find_all('span'):
                skill_text=''
                # case which will return title
                if 'class="mr1 t-bold"' in str(span):
                    title_list.append(span.span.text)
                # case which will return company
                elif 'class="t-14 t-normal"' in str(span):
                    company_list.append(span.span.text)
                # case which will return date
                elif 'class="t-14 t-normal t-black--light"' in str(span):
                    date_list.append(span.span.text)
                # case which will return summary or skills as summary
                else:
                    # summary case when there is no skills
                    if 'aria-hidden="true"' in str(span) and '<!-- -->Skills:<!-- -->' not in str(span):
                        # will look if summary was on list
                        if span.text not in (title_list+company_list+date_list+summary_list+skills_list):
                            summary_list.append(span.text)

                    # skills case
                    else:
                        if ('<!-- -->Skills:<!-- -->' in str(span)) and 'aria-hidden="true"' in str(span):
                            # will pull skills from text
                            skill_text=span.text
                            skill_text_list=skill_text.replace('Skills: ',' ').split('·')
                            skills_list = [value.strip() for value in skill_text_list]
            # tmp dict for exp
            tmp_exp_dict['company']=company_list[0]
            tmp_exp_dict['title']=title_list[0]
            tmp_exp_dict['date']=date_list[0]
            #if there is no summary
            if len(summary_list)==0:
                tmp_exp_dict['summary']=None
            # if there is summary
            else:
                tmp_exp_dict['summary']=summary_list[0]
            # if there arent any skills
            if len(skills_list)==0:
                tmp_exp_dict['skills']=None
            #if there are any skils
            else:
                tmp_exp_dict['skills']=skills_list

            #will append tmp dict to main list
            tmp_not_nested_exp_list.append(tmp_exp_dict)

    return tmp_not_nested_exp_list


def nested_experience(lis):
    # all nested experience's list
    nested_exp_list=list()

    # desired li
    desired_li_list=list()
    # loop of lis
    for li in lis:
        # infos where experiences are nested
        if 'class="scaffold-finite-scroll__content"' in str(li):
            # gets loop of the desired li
            for li1 in li.find_all(attrs={"class": "display-flex flex-column full-width align-self-center"}):
                # if li has id
                if li1.find_all(id=True):
                    desired_li_list.append(li1)


    for li in desired_li_list:
        tmp_company=None
        # to get all li tags
        span_list=li.find_all(attrs={"class":"mr1 hoverable-link-text t-bold"})
        for i in range(len(span_list)):
            # when i=0 it returns company
            if i==0:
                tmp_company=span_list[i].span.text
        # gets all divs which are elements of nested experience
        div_list=li.find_all("div",attrs={"class":"display-flex flex-column full-width align-self-center"})
        # loop for divs
        for div in div_list:
            tmp_experience_dict={'company':None,'title':None,'date':None,'summary':None,'skills':None}
            # nested temporary elements of experiences
            tmp_title=None
            tmp_date=None
            tmp_location=None
            tmp_summary=None
            tmp_skills=None
            skill_text=None
            skill_text_list=None
            # gets span list of the date and location
            date_and_location_span_list=div.find_all("span",attrs={"class":"t-14 t-normal t-black--light"})
            for i in range(len(date_and_location_span_list)):
                if i==0:
                    tmp_date=date_and_location_span_list[i].span.text
                elif i==2:
                    tmp_location=date_and_location_span_list[i].span.text
            # gets span list of the title
            title_span_list=div.find_all("span",attrs={"class":"mr1 hoverable-link-text t-bold"})
            for span in title_span_list:
                tmp_title=span.span.text

            # gets span list of the summary
            summary_and_skills_div_list=div.find_all("div",attrs={"class":"display-flex align-items-center t-14 t-normal t-black"})

            for i in range(len(summary_and_skills_div_list)):
                if i==0 and ('<!-- -->Skills:<!-- -->' not in str(summary_and_skills_div_list[i])):
                    # nested summary
                    tmp_summary=summary_and_skills_div_list[i].span.text
                if '<!-- -->Skills:<!-- -->' in str(summary_and_skills_div_list[i]):
                    #nested skills
                    skill_text=summary_and_skills_div_list[i].text
                    skill_text_list=skill_text.replace('Skills: ',' ').split('·')
                    tmp_skills = [value.strip() for value in skill_text_list]
            # all infos to tmp dictionary
            tmp_experience_dict['title']=tmp_title
            tmp_experience_dict['date']=tmp_date
            tmp_experience_dict['summary']=tmp_summary
            tmp_experience_dict['skills']=tmp_skills
            tmp_experience_dict['company']=tmp_company
            # tmp dict to nested_exp_list
            nested_exp_list.append(tmp_experience_dict)


    return nested_exp_list


def experience(experience_soup):
    '''
        Does:
            gets all info from experience section, splits nested and non-nested experiences,
            will run 2 different functions to work on them
        returns:
            experience_list: which includes non-nested and nested experience info
    '''
    try:
        # experience list which will contain all experience info
        experience_list=list()
        # list which will be used for temporary purposes
        tag_list=list()
        # body tag
        body=None
        # desired div section
        desired_div=None
        # gets the body
        body=experience_soup.body
        # list which will contain li tags from html codes
        lis=list()
        # gets all desired lis
        for li in body.find_all('li'):
            if 'li class="pvs-list__paged-list-item' in str(li):
                lis.append(li)

        # scrapes not nested experience info
        tmp_nested_exp_list=nested_experience(lis)
        # will put nested exp list to main experience_list
        experience_list+=tmp_nested_exp_list

        # scrapes not nested experience info
        tmp_not_nested_exp_list=not_nested_experience(lis)
        # will put not nested exp list to main experience_list
        experience_list+=tmp_not_nested_exp_list

        return experience_list
    except:
        return []
