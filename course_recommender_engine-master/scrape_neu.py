import os
import requests
import csv
import pandas as pd
from bs4 import BeautifulSoup

SCRAPE_DATA_PATH = 'data/neu_scraped_data/'

def scrape_neu_catalog(ms_course):
    """
    Function to fetch course catalog data (by default fetches MSDS course catalog)
    """
    catalog_url = 'http://catalog.northeastern.edu'
    degree = 'graduate'
    if ms_course == 'ds':
        school = 'computer-information-science'
        course = 'computer-science/data-science-ms'
    elif ms_course == 'da':
        school = 'professional-studies'
        course = 'masters-degree-programs/analytics-mps'
    elif ms_course == 'de':
        school = 'engineering'
        course = 'mechanical-industrial/data-analytics-engineering-ms'
    else:
        raise ValueError("Only query for ds, da or de courses")
    req_url = os.path.join(catalog_url, degree, school, course)
    req_soup = BeautifulSoup(requests.get(req_url).text, features="html.parser")
    course_list = []
    course_list.append(['Course Code', 'Course Name', 'Course Description'])
    tables = req_soup.find_all('table', {'class':'sc_courselist'})
    for i in range(len(tables)):
        course_names = []
        for course in tables[i].find('tbody').find_all('td', {'class':None, 'colspan':None}):
            course_names.append(course.contents[0])
        courses = tables[i].find('tbody').find_all('a', {'class':'bubblelink code'})
        for j in range(len(courses)):
            title = courses[j].get('title').split()
            desc_url = os.path.join(catalog_url,'search/?search=%s+%s'%(title[0], title[1]))
            course_soup = BeautifulSoup(requests.get(desc_url).text, features="html.parser")
            course_desc=''
            for x in course_soup.find_all('p', {'class':'courseblockdesc'})[-1].contents:
                course_desc = course_desc+str(x.string)
            course_list.append([courses[j].contents[0],  course_names[j], course_desc[1:-10]])

    file_name = os.path.join(SCRAPE_DATA_PATH, 'ms%s_courseinfo.csv'%ms_course)
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(course_list)
    courseinfo_df = pd.read_csv(file_name)
    return courseinfo_df