import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# import pymysql


basedir = os.path.abspath(os.path.dirname(__file__))

# Create the Connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_ECHO'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///final_proj.db' #using python
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pangeran123@localhost/sample_database'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://szpdnodkxhfdzi:1862c2d35185325156933e3a74178ece609fa5f782aa487c1d1a39247e26539b@ec2-52-86-56-90.compute-1.amazonaws.com:5432/d25hqmvif0hh52'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)