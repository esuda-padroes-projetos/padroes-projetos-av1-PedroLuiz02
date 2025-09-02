from flask import Flask
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from app.models import Usuario
from app.db import db 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = "B.D.C."

db.init_app(app)

login_manager = LoginManager(app)

login_manager.login_view = "login"

from app import routes