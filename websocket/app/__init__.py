from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
app.config['MONGO_URI'] = 'mongodb://mongo:27017/myapp'

mongo = PyMongo(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app import routes
