"""
Directors Controller
"""
import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
modelpath = os.path.dirname(current)+'\model'
sys.path.append(parent)
sys.path.append(modelpath)
sys.path.append(current)

from pymysql import IntegrityError
from schema import Directors,Movies, DirectorsSchema, DirectorsWithMoviesSchema, MoviesSchema
from config import db
from flask import abort,make_response
from response_payload import response
from sqlalchemy.exc import IntegrityError #for exception unique uid

def get_all(limit = None,offset = None):
    """
    Retrieve all director data with movies detail
    :param limit : set limit of query get
    :param offset : set offset of query get
    :return all director data with movie details
    """
    #if limit and offset is set
    if limit and offset:
        directors = Directors.query.order_by(Directors.name).limit(limit).offset(offset)
    #if limit and offset not set
    else:
        directors = Directors.query.order_by(Directors.name).all()
    data = DirectorsWithMoviesSchema(many=True).dump(directors)
    return response(
        status = 200, 
        data = data, 
        messages="all directors data retrieved succcesfully"
        )

def get_one(id):
    '''
    get only one Director by id
    :param id : set Director's id to fetch
    :return one row of director detail
    '''
    director = Directors.query.filter(Directors.id == id).one_or_none()
    if director:
        data = DirectorsSchema().dump(director)
        return response(status = 200, data = data, messages=f"get director by id : {id} success")
    else:
        return response(status = 400, messages=f"Unknown director id : {id}")
    # print(dir(director))
    
def update(id,request):
    '''
    update Director data by id
    :param id : id of director to update
    :request : JSON request for update director's data
    '''
    directorSelect =  Directors.query.get(id)
    if directorSelect and request is not None:
        schema = DirectorsSchema()
        try:
            input = schema.load(request, session=db.session)
        except Exception as e:
            abort(400,e.messages)
        input.id = directorSelect.id
        db.session.merge(input)
        db.session.commit()
    else:
        abort(404, f"Director not found for  id: {id}")
    return response(status = 201,messages = f"Update success for id {id}")

def delete(id):
    '''
    Delete Director by Director's id
    :param id : id of director to delete
    '''
    directorSelect =  Directors.query.filter(Directors.id == id).one_or_none()
    if directorSelect is not None:
        db.session.delete(directorSelect)
        db.session.commit()
        return response(status = 201, messages=f"Delete director by id : {id} success")
    else:
         return response(status = 400, messages=f"Director not found for id: {id}")
        # abort(404, f"Director not found for id: {id}")

def post(request):
    '''
    Post new Director Detail
    :param request : JSON request to post Director's data
    '''
    name = request.get('name')
    existing_director = Directors.query.filter(Directors.name == name).one_or_none()
    if existing_director is None:
        schema = DirectorsSchema()
        try:
            new_Director = schema.load(request, session = db.session)
        except Exception as e:
            # print(e.messages,e.normalized_messages)
            abort(404,e.messages)
        try:
            db.session.add(new_Director)
            db.session.commit()
            data = schema.dump(new_Director)
        except IntegrityError as e: #check if uid not double
            abort(400,"UID must be unique")
        return response(data=data, status=201, messages="new director added successfully")
    else:
        abort(400, f"Director for identity name: {name} already registered")

