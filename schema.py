from config import db,ma
from marshmallow import fields

class Directors(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    gender = db.Column(db.Integer)
    uid = db.Column(db.Integer)
    department = db.Column(db.String)
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
    original_title = db.Column(db.String)
    budget = db.Column(db.Integer)
    popularity = db.Column(db.Integer)
    release_date = db.Column(db.String)
    revenue = db.Column(db.Integer)
    title = db.Column(db.String)
    vote_average = db.Column(db.Integer)
    vote_count = db.Column(db.Integer)
    overview = db.Column(db.String)
    tagline = db.Column(db.String)
    uid = db.Column(db.Integer)
    director_id = db.Column(db.Integer,db.ForeignKey('directors.id'))

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
