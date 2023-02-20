from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xlsxwriter

import os
import re

global data
data = []


class Institution(object):
    institution_name = None
    website = None
    industry = None
    type = None
    headquarters = None
    company_size = None
    founded = None

    def __init__(self, name=None, website=None, industry=None, type=None, headquarters=None, company_size=None,
                 founded=None):
        self.name = name
        self.website = website
        self.industry = industry
        self.type = type
        self.headquarters = headquarters
        self.company_size = company_size
        self.founded = founded


class Experience(Institution):
    from_date = None
    to_date = None
    description = None
    position_title = None
    duration = None

    def __init__(self, from_date=None, to_date=None, description=None, position_title=None, duration=None,
                 location=None):
        self.from_date = from_date
        self.to_date = to_date
        self.description = description
        self.position_title = position_title
        self.duration = duration
        self.location = location

    def __repr__(self):
        return "{position_title} at {company} based at {location}".format(position_title=self.position_title,
                                                                          company=self.institution_name,
                                                                          location=self.location.split("\n", 1)[1])


class Education(Institution):
    from_date = None
    to_date = None
    description = None
    degree = None

    def __init__(self, from_date=None, to_date=None, description=None, degree=None):
        self.from_date = from_date
        self.to_date = to_date
        self.description = description
        self.degree = degree

    def __repr__(self):
        return "{degree} at {institution}".format(degree=self.degree, institution=self.institution_name)


class Scraper(object):
    driver = None

    def is_signed_in(self):
        try:
            self.driver.find_element_by_id("profile-nav-item")
            return True
        except:
            pass
        return False

    def __find_element_by_class_name__(self, class_name):
        try:
            self.driver.find_element_by_class_name(class_name)
            return True
        except:
            pass
        return False

    def __find_element_by_xpath__(self, tag_name):
        try:
            self.driver.find_element_by_xpath(tag_name)
            return True
        except:
            pass
        return False


class Person(Scraper):
    __TOP_CARD = "pv-top-card"
    name = None
    experiences = []
    educations = []
    location = None
    also_viewed_urls = []
    linkedin_url = None

    def time_divide(string):
        duration = re.search("\((.*?)\)", string)

        if duration != None:
            duration = duration.group(0)
            string = string.replace(duration, "").strip()
        else:
            duration = "()"
            string = string + "––()"

        times = string.split("–")
        return (times[0].strip(), times[1].strip(), duration[1:-1])

    def __init__(self, linkedin_url=None, name=None, experiences=[], educations=[], driver=None, get=True, scrape=True):
        self.linkedin_url = linkedin_url
        self.name = name
        self.experiences = experiences or []
        self.educations = educations or []

        if driver is None:
            try:
                if os.getenv("CHROMEDRIVER") == None:
                    driver_path = os.path.join(os.path.dirname(__file__), 'drivers/chromedriver')
                else:
                    driver_path = os.getenv("CHROMEDRIVER")

                driver = webdriver.Chrome(driver_path)
            except:
                driver = webdriver.Chrome()

        if get:
            driver.get(linkedin_url)

        self.driver = driver

        if scrape:
            self.scrape()

    def add_experience(self, experience):
        self.experiences.append(experience)

    def add_education(self, education):
        self.educations.append(education)

    def add_location(self, location):
        self.location = location

    def scrape(self, close_on_complete=True):
        if self.is_signed_in():
            self.scrape_logged_in(close_on_complete=close_on_complete)
        else:
            self.scrape_not_logged_in(close_on_complete=close_on_complete)

    def scrape_logged_in(self, close_on_complete=True):
        driver = self.driver
        root = driver.find_element_by_class_name(self.__TOP_CARD)
        self.name = root.find_elements_by_xpath("//section/div/div/div/*/li")[0].text.strip()

        driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));")

        _ = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "experience-section")))

        # get experience
        exp = driver.find_element_by_id("experience-section")
        for position in exp.find_elements_by_class_name("pv-position-entity"):
            position_title = position.find_element_by_tag_name("h3").text.strip()
            company = position.find_element_by_class_name("pv-entity__secondary-title").text.strip()

            try:
                times = position.find_element_by_class_name("pv-entity__date-range").text.strip()
                times = "\n".join(times.split("\n")[1:])
                from_date, to_date, duration = time_divide(times)
            except:
                from_date, to_date, duration = ("Unknown", "Unknown", "Unknown")
            try:
                location = position.find_element_by_class_name("pv-entity__location").text.strip()
            except:
                location = None
            experience = Experience(position_title=position_title, from_date=from_date, to_date=to_date,
                                    duration=duration, location=location)
            experience.institution_name = company
            self.add_experience(experience)

        # get location
        location = driver.find_element_by_class_name(f'{self.__TOP_CARD}--list-bullet')
        location = location.find_element_by_tag_name('li').text
        self.add_location(location)

        driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/1.5));")

        _ = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "education-section")))

        # get education
        edu = driver.find_element_by_id("education-section")
        for school in edu.find_elements_by_class_name("pv-education-entity"):
            university = school.find_element_by_class_name("pv-entity__school-name").text.strip()
            degree = "Unknown Degree"
            try:
                degree = school.find_element_by_class_name("pv-entity__degree-name").text.strip()
                times = school.find_element_by_class_name("pv-entity__dates").text.strip()
                from_date, to_date, duration = time_divide(times)
            except:
                from_date, to_date = ("Unknown", "Unknown")
            education = Education(from_date=from_date, to_date=to_date, degree=degree)
            education.institution_name = university
            self.add_education(education)

        if close_on_complete:
            driver.quit()
        print("*** Data Scraped ***")
        data.append(self.name)
        data.append(self.linkedin_url)
        data.append(self.location)
        data.append(self.experiences)
        data.append(self.educations)

    def scrape_not_logged_in(self, close_on_complete=True, retry_limit=10):
        driver = self.driver
        retry_times = 0
        while self.is_signed_in() and retry_times <= retry_limit:
            page = driver.get(self.linkedin_url)
            retry_times = retry_times + 1

        # get name
        self.name = driver.find_element_by_id("name").text.strip()

        # get experience
        exp = driver.find_element_by_id("experience")
        for position in exp.find_elements_by_class_name("position"):
            position_title = position.find_element_by_class_name("item-title").text.strip()
            company = position.find_element_by_class_name("item-subtitle").text.strip()

            try:
                times = position.find_element_by_class_name("date-range").text.strip()
                from_date, to_date, duration = time_divide(times)
            except:
                from_date, to_date, duration = (None, None, None)

            try:
                location = position.find_element_by_class_name("location").text.strip()
            except:
                location = None
            experience = Experience(position_title=position_title, from_date=from_date, to_date=to_date,
                                    duration=duration, location=location)
            experience.institution_name = company
            self.add_experience(experience)

        # get education
        edu = driver.find_element_by_id("education")
        for school in edu.find_elements_by_class_name("school"):
            university = school.find_element_by_class_name("item-title").text.strip()
            degree = school.find_element_by_class_name("original").text.strip()
            try:
                times = school.find_element_by_class_name("date-range").text.strip()
                from_date, to_date, duration = time_divide(times)
            except:
                from_date, to_date = (None, None)
            education = Education(from_date=from_date, to_date=to_date, degree=degree)
            education.institution_name = university
            self.add_education(education)

        # get
        if close_on_complete:
            driver.quit()

    def __repr__(self):
        return "{name}\n\nExperience\n{exp}\n\nEducation\n{edu}".format(name=self.name, exp=self.experiences,
                                                                        edu=self.educations)


class Scrape():
    def getData(self):
        driver = webdriver.Chrome('Path/To/chromedriver/chromedriver.exe')
        email = "some@email.address"  # Enter username of linkedin account here
        password = "SOMEPASSWORD"  # Enter Password of linkedin account here
        if not email or not password:
            email, password = __prompt_email_password()
        driver.get('https://www.linkedin.com/login')
        driver.find_element_by_id('username').send_keys(email)
        driver.find_element_by_id('password').send_keys(password)
        driver.find_element_by_xpath("//*[@type='submit']").click()
        person = Person("https://www.linkedin.com/in/someprofile", driver=driver)  # Enter LinkedIn profile url of user

    def writeData(self):
        workbook = xlsxwriter.Workbook("linkedin-data.xlsx")
        worksheet = workbook.add_worksheet('User')
        bold = workbook.add_format({'bold': True})
        worksheet.write(0, 0, 'Name', bold)
        worksheet.write(0, 1, 'Profile', bold)
        worksheet.write(0, 2, 'Location', bold)
        worksheet.write(0, 3, 'Experiences', bold)
        worksheet.write(0, 4, 'Educations', bold)

        try:
            worksheet.write(1, 0, data[0])
        except:
            pass
        try:
            worksheet.write(1, 1, data[1])
        except:
            pass
        try:
            worksheet.write(1, 2, data[2])
        except:
            pass
        try:
            j = 0
            for i in range(1, len(data[3]) + 1):
                worksheet.write(i, 3, str(data[3][j]))
                j = j + 1
        except:
            pass
        try:
            j = 0
            for i in range(1, len(data[4]) + 1):
                worksheet.write(i, 4, str(data[4][j]).split("\n", 1)[1])
                j = j + 1
        except:
            pass

        workbook.close()

    def start(self):
        self.getData()
        self.writeData()


if __name__ == "__main__":
    obJH = Scrape()
    obJH.start()
