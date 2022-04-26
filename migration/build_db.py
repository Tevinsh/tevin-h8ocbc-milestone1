'''
Module for Migrating data
'''
import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
modelpath = os.path.dirname(current)+'\model'
sys.path.append(parent)
sys.path.append(modelpath)

import os
from config import db
from schema import Movies,Directors
import json

#instantiate data from json file
f = open('directors.json',encoding='utf-8')
g = open('movies.json',encoding='utf-8')
directors_data = json.load(f)
movies_data = json.load(g)


# Delete database file if it exists currently #if using sqlite
# if os.path.exists('final_proj.db'):
#     os.remove('final_proj.db')

#create db from schema
db.create_all()

#add row from directors_data and movies_data
for director in directors_data:
    d = Directors(
        department=director['department'], 
        gender=director['gender'], 
        id = director['id'], 
        name = director['name'], 
        uid = director['uid'])
    db.session.add(d)

for movies in movies_data:
    m = Movies(
        budget=movies['budget'],
        director_id=movies['director_id'],
        id = movies['id'],
        original_title = movies['original_title'],
        overview = movies['overview'],
        popularity = movies['popularity'],
        release_date = movies['release_date'],
        revenue = movies['revenue'],
        tagline = movies['tagline'],
        title = movies['title'],
        uid = movies['uid'],
        vote_average = movies['vote_average'],
        vote_count = movies['vote_count']
        )
    db.session.add(m)

#commiting session
db.session.commit()