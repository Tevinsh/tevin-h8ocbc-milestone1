# from numbers import Real
# from typing import Text
# from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey
# from sqlalchemy.orm import declarative_base,relationship,sessionmaker
# from sqlalchemy.ext.automap import automap_base #auto map for existing database
# Base = automap_base() #automap
# engine = create_engine('sqlite:///final_proj.db', echo = True)
# conn = engine.connect()

# class Directors(Base):
#     __tablename__ = 'directors'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     gender = Column(Integer)
#     uid = Column(Integer)
#     department = Column(String)

# class Movies(Base):
#     __tablename__ = 'movies'

#     id = Column(Integer, primary_key=True)
#     originla_title = Column(String)
#     budget = Column(Integer)
#     popularity = Column(Integer)
#     release_date = Column(Integer)
#     revenue = Column(Integer)
#     title = Column(String)
#     vote_average = Column(Integer)
#     vote_count = Column(Integer)
#     overview = Column(String)
#     tagline = Column(String)
#     uid = Column(Integer)
#     director_id = Column(ForeignKey('movies.id'))

# Base.prepare(engine, reflect=True)


# Session = sessionmaker(bind=engine)
# session = Session()
