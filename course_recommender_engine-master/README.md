# Course Recommendation Engine
DS5230 Project: Course Recommender Engine

## File: courseRecommender.py

To run the course recommendation engine, run the piece of code below (You can try different input strings by setting the ```userInput``` variable):

```
from courseRecommender import CourseRecommender
userInput = 'oracle sql, python, machine learning, natural language processing, data science'
recommender =CourseRecommender()
print(recommender.recommendCourses(userInput))
```
Expected output:
```
Initiating Course Recommendation Engine
Starting course recommendation Engine at  2020-04-15 15:15:30.582050
Recommendation Process Complete, duration:  0:00:55.003680

['Dynamic Modeling for Environmental Decision Making', 
'Geographic Information Systems for Urban and Regional Policy', 
'Empirical Research Methods', 
'Biostatistics in Public Health', 
'Computational Physics', 
'Introduction to Epidemiology', 
'Advanced Machine Learning', 
'Research Design', 
'Time Series and Geospatial Data Sciences', 
'Advanced Computer Vision']
```

# Logistics

Detailed git instruction (PLEASE READ IF YOU DON'T USE GIT REGULARLY):
https://gist.github.com/blackfalcon/8428401

### How-to for devs
### First time (once)
1. Clone the repo
2. use checkout command to switch to your personal branch (DO NOT DIRECTLY MAKE CHANGES TO MASTER BRANCH)
3. cd course_recommender_engine
4. Create two directories:
	1. `data/indeed-dataset-data-scientistanalystengineer`
	2. `data/neu_scraped_data`
5. Add the indeed's data from kaggle in the `3(i)` directory we created above

### Any other times
1. Make your changes
2. git add *
3. git commit -m "Commit message"
4. git pull origin master
5. git push origin master

Create a pull request to merge your code to master branch.
