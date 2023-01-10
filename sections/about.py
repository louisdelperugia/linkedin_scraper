from bs4 import BeautifulSoup

def about(about_section):
    '''
        Does:
            gets summary from the linkedin profile

        returns:
            summary (str)
    '''
    try:
        summary=None
        if about_section!=None:
            for div in about_section.find_all('div'):
                if 'class="display-flex ph5 pv3"' in str(div):
                    for span in div.find_all('span'):
                        if 'aria-hidden="true"' in str(span):
                            summary=span.text

        return summary
    except:
        return None
