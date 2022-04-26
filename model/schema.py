import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
modelpath = os.path.dirname(current)+'/model'
sys.path.append(parent)
sys.path.append(modelpath)

from enum import unique
from config import db,ma
from marshmallow import fields

class Directors(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    gender = db.Column(db.Integer, nullable=False)
    uid = db.Column(db.Integer, nullable=False, unique=True)
    department = db.Column(db.String(32), nullable=False)
    movies = db.relationship(
        'Movies',
        backref='directors',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(Movies.popularity)'
    )

class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    original_title = db.Column(db.String(100),nullable=False)
    budget = db.Column(db.Integer,nullable=False)
    popularity = db.Column(db.Integer,nullable=False)
    release_date = db.Column(db.String(32),nullable=False)
    revenue = db.Column(db.BigInteger,nullable=False)
    title = db.Column(db.String(100),nullable=False)
    vote_average = db.Column(db.Integer,nullable=False)
    vote_count = db.Column(db.Integer,nullable=False)
    overview = db.Column(db.String(1000)) #remove nullable=false
    tagline = db.Column(db.String(1000)) #remove nullable=false
    uid = db.Column(db.Integer,nullable=False,unique=True)
    director_id = db.Column(db.Integer,db.ForeignKey('directors.id'),nullable=False)

class DirectorsSchema(ma.SQLAlchemyAutoSchema):
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    class Meta:
        model = Directors
        load_instance = True
        include_relationship = True

class MoviesSchema(ma.SQLAlchemyAutoSchema):
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    class Meta:
        model = Movies
        load_instance = True
        include_relationship = True

class DirectorsWithMoviesSchema(ma.SQLAlchemyAutoSchema):
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    class Meta:
        model = Directors
        load_instance = True
        include_relationship = True
    movies = fields.Nested(MoviesSchema,default=[],many=True)
