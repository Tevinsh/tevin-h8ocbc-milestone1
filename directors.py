from schema import Directors,Movies, DirectorsSchema, DirectorsWithMoviesSchema, MoviesSchema
from config import db
from flask import abort,make_response
# from sqlalchemy import or_
from response_payload import response

def get_all():
    # Create the list of people from our data
    directors = Directors.query.order_by(Directors.name).all()
    data = DirectorsWithMoviesSchema(many=True).dump(directors)
    # return data,200
    return response(status = 200, data = data, messages="all directors retrieved succcesfully")

def get_one(id):
    director = Directors.query.filter(Directors.id == id).one_or_none()
    data = DirectorsSchema().dump(director)
    print(dir(director))
    return response(status = 200, data = data, messages=f"get director by id : {id} success")

def update(id,request):
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
    return f"Update success for id{id}",200

def delete(id):
    directorSelect =  Directors.query.filter(Directors.id == id).one_or_none()
    if directorSelect is not None:
        db.session.delete(directorSelect)
        db.session.commit()
        return response(status = 200, messages=f"get director by id : {id} success")
    else:
         return response(status = 404, messages=f"Director not found for id: {id}")
        # abort(404, f"Director not found for id: {id}")

def post(request):
    name = request.get('name')
    # id = request.get('id')
    # print(name,id)
    existing_director = Directors.query.filter(Directors.name == name).one_or_none()
    # print("existing diretor is: ",existing_director)
    # for i in existing_director:
    #     print(i)
    if existing_director is None:
        schema = DirectorsSchema()
        try:
            new_Director = schema.load(request, session = db.session)
        except Exception as e:
            # print(e.messages,e.normalized_messages)
            abort(404,e.messages)
        db.session.add(new_Director)
        db.session.commit()
        data = schema.dump(new_Director)
        return data, 200
    else:
        abort(404, f"Director for identity name: {name} id: {id} already registered")

def new():
    return 'success'