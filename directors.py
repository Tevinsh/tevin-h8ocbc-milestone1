from schema import Directors,Movies, DirectorsSchema, DirectorsWithMoviesSchema, MoviesSchema
from config import db
from flask import abort,make_response
from sqlalchemy import or_
from response_payload import response

def get_all():
    # Create the list of people from our data
    directors = Directors.query.order_by(Directors.name).all()
    data = DirectorsWithMoviesSchema(many=True).dump(directors)
    # return data,200
    return response(status = 200, data = data)

def get_one(id):
    director = Directors.query.get(id)
    data = DirectorsSchema().dump(director)
    print(dir(director))
    return data,200

def update(id,request):
    directorSelect =  Directors.query.get(id)
    if directorSelect and request is not None:
        schema = DirectorsSchema()
        input = schema.load(request, session=db.session)
        input.id = directorSelect.id
        db.session.merge(input)
        db.session.commit()
    else:
        abort(404, f"Director not found for  id: {id}")
    return f"Update success for id{id}",200

def delete(id):
    directorSelect =  Directors.query.get(id)
    if directorSelect is not None:
        db.session.delete(directorSelect)
        db.session.commit()
        return make_response(f"Director with id {id} deleted")
    else:
        abort(404, f"Director not found for id: {id}")

def post(request):
    name = request.get('name')
    id = request.get('id')
    existing_director = Directors.query.filter(Directors.name == name).filter(Directors.id == id)
    for i in existing_director:
        print(i.name)
    if existing_director is None:
        schema = DirectorsSchema()
        new_Director = schema.load(request, session = db.session)
        db.session.add(new_Director)
        db.session.commit()
        data = schema.dump(new_Director)
        return data, 200
    else:
        abort(404, f"Director for identity name: {name} id: {id} already registered")

def new():
    return 'success'