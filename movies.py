from schema import Directors,Movies, DirectorsSchema, DirectorsWithMoviesSchema, MoviesSchema
from config import db
from flask import abort,make_response
from sqlalchemy import or_
from response_payload import response

def get_all():
    movies = Movies.query.all()
    data = MoviesSchema(many=True).dump(movies)
    return data,200

# director/{director_id}/movies
def get_director_movies(director_id):
    # print(director_id)
    movies = Movies.query.join(Directors, Movies.director_id == Directors.id).filter(Directors.id == director_id).all()
    print(dir(movies))
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
        director.movies.append(new_movie)
        db.session.commit()
        data = schema.dump(new_movie)
    return response(
                status = 201, 
                data = data,
                messages=f"Success add movies for director_id : {director_id}"
                )

def delete(id):
    movies = Movies.query.filter(Movies.id == id).one_or_none()
    if movies is not None:
        db.session.delete(movies)
        db.session.commit()
        return response(status = 201, messages = f"Movies for id : {id} Succesfully deleted")
    else:
        return response(status = 404, messages = f"Movies id : {id} not found")

def put(id, request):
    moviesSelect = Movies.query.filter(Movies.id == id).one_or_none()
    if moviesSelect is not None:
        schema = MoviesSchema()
        try:
            input = schema.load(request, session=db.session)
        except Exception as e:
            return response(400, messages = e.messages)
        input.id = moviesSelect.id
        db.session.merge(input)
        db.session.commit()
        return response(status = 201,messages = f"Update Success for id :{id}")
    else:
        return response(status = 404, messages = f"Movies not found for id: {id}")
