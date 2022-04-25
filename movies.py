from schema import Directors,Movies, DirectorsSchema, DirectorsWithMoviesSchema, MoviesSchema
from config import db
from flask import abort,make_response
from sqlalchemy import or_

def get_all():
    movies = Movies.query.all()
    data = MoviesSchema(many=True).dump(movies)
    return data,200

def get_one(id):
    movies = Movies.query.get(id)
    data = MoviesSchema().dump(movies)
    return data,200

def post(director_id,request):
    director = Directors.query.filter(Directors.id == director_id).one_or_none()
    if director is None:
        abort(404, f"Director not found, failed to get Director with id : {director_id}")
    else:
        schema = MoviesSchema()
        new_movie = schema.load(request, session=db.session)
        director.movies.append(new_movie)
        db.session.commit()
        data = schema.dump(new_movie)
    return data,201

def delete(id):
    movies = Movies.query.filter(Movies.id == id).one_or_none()
    if movies is not None:
        db.session.delete(movies)
        db.session.commit()
        return f"Movies for id : {id} Succesfully deleted",201
    else:
        abort(404,f"Movies id : {id} not found")

def put(id, request):
    moviesSelect = Movies.query.filter(Movies.id == id).one_or_none()
    if moviesSelect is not None:
        schema = MoviesSchema()
        input = schema.load(request, session=db.session)
        input.id = moviesSelect.id
        db.session.merge(input)
        db.session.commit()
        return f"Update Success for id :{id}",200
    else:
        abort(404, f"Movies not found for id: {id}")
