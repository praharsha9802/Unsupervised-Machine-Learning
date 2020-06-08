import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans

from bs4 import BeautifulSoup
from pylab import *

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

import nltk
from gensim.models import Word2Vec

from datetime import datetime

import warnings
warnings.filterwarnings("ignore")

import os
import requests
import csv


class CourseRecommender():
    
    def __init__(self):
        print('Initiating Course Recommendation Engine')    
        self.vectorize = CountVectorizer(max_features=10)
        self.clusterCount = 3 
        self.maxIter = 600
        self.kmeans = KMeans(n_clusters=self.clusterCount, max_iter=self.maxIter, algorithm = 'auto')
        self.jobData = self.getJobData()
        self.jobData_cleaned = self.process(self.jobData)
        
        self.conv = lambda i : i or '' 
        self.jobData_cleaned = [self.conv(i) for i in self.jobData_cleaned]
        self.jobData_cleaned = pd.Series((i for i in self.jobData_cleaned)) 
        self.jobData_vecs = self.vectorize.fit_transform(self.jobData_cleaned)
        
        self.fitted = self.kmeans.fit(self.jobData_vecs)
        self.prediction = self.kmeans.predict(self.jobData_vecs)

    
    
    def recommendCourses(self, userInput):
        """
        userInput: a list of skills should be comma separated string
        """
        startTime = datetime.now()
        print('Starting course recommendation Engine at ',startTime)
        inp = self.preprocessText(userInput)
        input_cleaned = pd.Series(inp) 
        in_vec = self.vectorize.fit_transform(input_cleaned)
        user_pred = self.kmeans.predict(in_vec)

        cluster_1 = []
        for i in range(len(self.jobData_cleaned)):
            if self.prediction[i] == user_pred:
                cluster_1.append({'index':i, 'data':self.jobData_cleaned[i]})
        cluster_1 = pd.DataFrame(cluster_1)

        msds_df = self.getNeuCourseCatalogData()[0]
        course_description_raw = msds_df['Course Description']
        course_description_cleaned = [self.preprocessText(x) for x in course_description_raw]
        course_description_cleaned = [self.conv(i) for i in course_description_cleaned]
        course_description_cleaned = pd.Series((i for i in course_description_cleaned)) 
        course_vecs = self.vectorize.fit_transform(course_description_cleaned)
        
        cluster_data_vectorized = self.vectorize.fit_transform(cluster_1['data'])
        similarity = cosine_similarity(cluster_data_vectorized, course_vecs)

        top_sims = []

        for i in range(len(similarity)):
            for j in range(len(similarity[0])):
                    top_sims.append({'job':i,'course':j,'sim':similarity[i][j]})

        top_sims=pd.DataFrame(top_sims)
        
        top_sims = top_sims.drop_duplicates(subset='course', keep="last")
        top_sims = top_sims.sort_values('sim', ascending=False)

        courseList = []
        for i in top_sims[:10].course:
            courseList.append(msds_df.iloc[i]['Course Name'])

        print('Recommendation Process Complete, duration: ',datetime.now()-startTime)    
        return courseList
    
    def getJobData(self):
        file_location = 'data/indeed-dataset-data-scientistanalystengineer/indeed_job_dataset.csv'
        indeed_raw = pd.read_csv(file_location)
        description_raw = indeed_raw.Description
        return description_raw
    
    def process(self, data):
        data = [self.cleanHTMLtext(x) for x in data]
        data = [self.preprocessText(x) for x in data]
        return data
        
        
    def cleanHTMLtext(self, raw_html):
        """
        Function to clean the Description Col in Indeed Dataset
        """
        if type(raw_html)==str:
            cleantext = BeautifulSoup(raw_html).get_text(" ")
            #BeautifulSoup(raw_html, "html.parser").text
            cleantext = cleantext.replace('\r', ' ').replace('\n', ' ')[1:-1]
            re.sub('\W+', ' ', cleantext)
            re.sub(',', ' ', cleantext)
            return cleantext
        else:
            return None

    def stemSentence(self, sentence, porter):
        token_words=nltk.word_tokenize(sentence)
        token_words
        stem_sentence=[]
        for word in token_words:
            stem_sentence.append(porter.stem(word))
            stem_sentence.append(" ")
        return "".join(stem_sentence)


    def preprocessText(self, text, remove_period=True):
        porter=PorterStemmer()
        lemmatizer=WordNetLemmatizer()
        if type(text)==str:
            text = text.lower().strip()
            stemmed_sentence = self.stemSentence(text, porter)
            tokenize = nltk.word_tokenize(text)
            lemmatize_tokens = [lemmatizer.lemmatize(word) for word in tokenize]
            stop_words = stopwords.words('english')
            remove_stopwords = [w for w in lemmatize_tokens if not w in stop_words]
            if remove_period:
                remove_punctuation = [word for word in remove_stopwords if word.isalpha() or word == '.']
            else:
                remove_punctuation = [word for word in remove_stopwords if word.isalpha()]
            return " ".join(remove_punctuation)
        else:
            return None
        
        
    def getNeuCourseCatalogData(self):
        msds_df = self.scrape_neu_catalog('ds')
        msda_df = self.scrape_neu_catalog('da')
        msde_df = self.scrape_neu_catalog('de')
        catalog = [msds_df,msda_df,msde_df]
        return catalog
        
        
    def scrape_neu_catalog(self, ms_course, SCRAPE_DATA_PATH='data/neu_scraped_data/'):
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

    


        
        