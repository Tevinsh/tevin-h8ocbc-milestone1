'''
Movies Controller
'''
import os
import sys

import sqlalchemy
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
modelpath = os.path.dirname(current)+'/model'
sys.path.append(parent)
sys.path.append(modelpath)
sys.path.append(current)

from schema import Directors,Movies, DirectorsSchema, DirectorsWithMoviesSchema, MoviesSchema
from config import db
from flask import abort,make_response
from sqlalchemy import or_
from response_payload import response
from sqlalchemy.exc import IntegrityError #for exception unique uid

def get_all(limit = None,offset = None):
    '''
    get all movies data
    :param limit : set limit of data, default null
    :param offset : set offset of data, default null
    :return all Movies data 
    '''
    if limit and offset:
        movies = Movies.query.limit(limit).offset(offset)
        print('called')
    else:
        movies = Movies.query.all()
    data = MoviesSchema(many=True).dump(movies)
    return response(
                    status = 200,
                    data = data, 
                    messages= "success get all movies"
                    )

# director/{director_id}/movies
def get_director_movies(director_id):
    '''
    get list of movies directed by director_id
    :param director_id: director's id
    '''
    movies = Movies.query.join(Directors, Movies.director_id == Directors.id).filter(Directors.id == director_id).all()
    if movies:
        schema = MoviesSchema(many = True)
        data = schema.dump(movies)
        return response(
            status = 200, 
            data = data,
            messages=f"Success get movies from director_id : {director_id}"
            )
    else:
        return response(
            status = 404, 
            messages=f"Data not found for director_id : {director_id}"
            )

# movies/{movies_id}/directordetail
def get_director_from_movies(movies_id):
    '''
    Get director detail from movies
    :param movies_id: movies's id
    :return movie director detail
    '''
    director = Directors.query.join(Movies, Movies.director_id == Directors.id).filter(Movies.id == movies_id).one_or_none()
    if director is not None:
        schema = DirectorsSchema()
        data = schema.dump(director)
        return response(
            status = 200, 
            data = data,
            messages=f"Success get movies from movies_id : {movies_id}"
            )
    else:
        return response(
            status = 404, 
            messages=f"Unknown movies_id : {movies_id}"
            )

def get_one(id):
    '''
    Get one movies detail by id
    :param id: id of movies to get
    '''
    movies = Movies.query.filter(Movies.id == id).one_or_none()
    if movies is not None:
        data = MoviesSchema().dump(movies)
        return response(
                status = 200, 
                data = data,
                messages=f"Success get movies from id : {id}"
                )
    else:
        return response(
                status = 404, 
                messages=f"Unknown movies for id : {id}"
                )

def post(director_id,request):
    '''
    Post a movie detail based on director_id an request JSON
    :param director_id : director's id
    :param request: JSON request to post movie data
    '''
    director = Directors.query.filter(Directors.id == director_id).one_or_none()
    if director is None:
        return response(
                status = 404, 
                messages=f"Director not Found for id : {director_id}"
                )
    else:
        schema = MoviesSchema()
        try:
            new_movie = schema.load(request, session=db.session)
        except Exception as e:
            return abort(400,e.messages)
        try:
            director.movies.append(new_movie)
            db.session.commit()
            data = schema.dump(new_movie)
        except IntegrityError:
            return abort(400,'UID already exist') 
    return response(
                status = 201, 
                data = data,
                messages=f"Success add movies for director_id : {director_id}"
                )

def delete(id):
    '''
    delete movies by id
    :param id: movie id
    '''
    movies = Movies.query.filter(Movies.id == id).one_or_none()
    if movies is not None:
        db.session.delete(movies)
        db.session.commit()
        return response(
            status = 201, 
            messages = f"Movies for id : {id} Succesfully deleted"
            )
    else:
        return response(status = 404, messages = f"Movies id : {id} not found")

def put(id, request):
    '''
    Update existing movie by id movie and JSON request
    :param id: movie id
    :param request: JSON request to update movie
    '''
    moviesSelect = Movies.query.filter(Movies.id == id).one_or_none()
    if moviesSelect is not None:
        schema = MoviesSchema()
        try:
            input = schema.load(request, session=db.session)
        except Exception as e:
            return response(400, messages = e.messages)
        input.id = moviesSelect.id
        try:
            db.session.merge(input)
            db.session.commit()
        except IntegrityError:
            return abort(400,'UID already exist')
        return response(
            status = 201,
            messages = f"Update Success for id :{id}"
            )
    else:
        return response(
            status = 404, 
            messages = f"Movies not found for id: {id}"
            )
