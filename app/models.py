from app.db import db
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False)
    senha = db.Column(db.String(), nullable=False)
