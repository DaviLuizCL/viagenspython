from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SECRET_KEY'] = '738c359d905a2063b0bbffd11a30de51'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meusite.db'

database = SQLAlchemy(app)

from estudoboladao import routes