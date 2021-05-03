from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

login_manager = LoginManager()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mykey'

basedir = os.path.abspath( os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(basedir,'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db=SQLAlchemy(app)

Migrate(app,db)

login_manager.init_app(app)
login_manager.login_view = 'login'