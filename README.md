# Moneyball

## Overview
In this project we have gathered baseball player statistics from the built in python library, pybaseball, to utilize in training a supervised machine learning model in order to predict if a player will be made MVP.<br>
- Selected Topic --- Baseball
- Reason of selecting topic --- There is a vast amount of statistical data in baseball and we believe this will help in creating a well trained prediction model.
- Description of source data --- Our data was gathered from a built in python library, pybaseball. This library was developed by James LeDoux, a data scientist and armchair sabermetrician.
- Question to answer --- Can we predict an MVP based on a player's batting statistics?<br>

## Project Outline

### Communication Protocols
We will communicate primarly through Slack using a separtate group message. We will meet during class time 2 times a week to discuss where each of are at in our project. 

### Technologies to be Used
Language: Python, and SQL

Interpreter: Jupyter Notebook

Packages: from pybaseball import batting_stats_range
          from pybaseball import batting_stats
          from pathlib import Path
          from sklearn import LogisticRegression
	    from sklearn.model_selection import train_test_split


Libraries: import numpy as np
           import pandas as pd          

Database: Direct import into PostgreSQL

Machine Learning Model: Logistic Regression Model

### Database
We have set up a database in PostgreSQL to hold our data. This was done with SQLAlchemy importing the dataframes directly into Postgre from our initial ETL notebook.

### Machine Learning Model
- Which model did you choose and why?
We currently have selected the Logistic Regression Model because we are looking to predict if a player will be made MVP or not based on that seasons batting stats.
- How are you training your model?
We are using the train test split package from sklearn
- What is the model's accuracy?
Our model's accuracy is
- How does this model work?


	