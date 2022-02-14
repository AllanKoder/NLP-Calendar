from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
#create the application object 
app = Flask(__name__)

#configuration of the secret key for the database for hashing   
app.config["SECRET_KEY"] = "cba86843291e29d0ab0c88abed3a6df3"
#set the location of the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginManager = LoginManager(app)

from calendarweb import routes
