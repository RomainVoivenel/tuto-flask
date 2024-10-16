from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
import os.path
app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SECRET_KEY'] = '079d3e12-a2bd-490b-927b-4f5b45a656ab'
bootstrap = Bootstrap5(app)

def mkpath(p):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), p))

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///'+mkpath('../myapp.db')
)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)