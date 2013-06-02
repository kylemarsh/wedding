from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('wedding.cfg')

db = SQLAlchemy(app)


#import wedding.models
import wedding.views
