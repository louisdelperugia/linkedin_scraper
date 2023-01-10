from bs4 import BeautifulSoup

def parent_tag(tag_list):
    '''
        Does:
            returns biggest tag from list, will compare their lenght
    '''
    tmp_tag=''
    for element in tag_list:
        if len(tmp_tag)<len(str(element)):
            tmp_tag=element
    return tmp_tag


def div_till_section(body):
    count=0
    # first div
    for div in body:
        if 'class="application-outlet"' in str(div):
            desired_div=div

    #second div
    for div in desired_div.find_all('div'):
        if 'class="authentication-outlet"' in str(div):
            desired_div=div

    for div in desired_div.find_all('div'):
        if 'id="profile-content"' in str(div):
            desired_div=div

    for div in desired_div.find_all('div'):
        if 'class="body"' in str(div):
            desired_div=div

    tag_list=list()
    for div in desired_div.find_all('div'):
        if 'id="main"' in str(div):
            tag_list.append(div)
    div=parent_tag(tag_list)
    desired_div=div
    # print(desired_div)
    # exit()
    # for div in desired_div.find_all('div'):
    #     if 'id="main"' in str(div):
    #         desired_div=div
    #         print(desired_div)

    for div in desired_div.find_all('div'):
        if 'class="scaffold-layout__inner scaffold-layout-container' in str(div):
            desired_div=div

    for div in desired_div.find_all('div'):
        if 'class="scaffold-layout__row scaffold-layout__content' in str(div):
            desired_div=div
    for div in desired_div.find_all('main'):
        if 'id="main"' in str(div):
            desired_div=div

    return div
