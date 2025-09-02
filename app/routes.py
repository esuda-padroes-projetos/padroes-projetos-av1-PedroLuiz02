from app import app, login_manager
from flask import render_template, jsonify, request, redirect, url_for
from app.models import Usuario
from flask_login import login_user, login_required, logout_user, current_user
from app.db import db 
import hashlib

def hash(txt):
    hash_obj = hashlib.sha256(txt.encode('utf-8'))
    return hash_obj.hexdigest()


@login_manager.user_loader
def user_loader(user_id):
    return db.session.get(Usuario, int(user_id))


@app.route('/')
def home():
    if current_user.is_authenticated:
        print(current_user.nome)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['emailForm']
        senha = request.form['senhaForm']

        user = db.session.query(Usuario).filter_by(email=email, senha=hash(senha)).first()
        if not user:
            return 'Email ou senha incorretos.'
        
        login_user(user)
        return redirect(url_for('home'))
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        nome = request.form['nomeForm']
        email = request.form['emailForm']
        senha = request.form['senhaForm']
        confirm_senha = request.form['confirm_senhaForm']

        novo_usuario = Usuario(nome=nome, email=email, senha=hash(senha))
        db.session.add(novo_usuario)
        db.session.commit()

        login_user(novo_usuario)

        return redirect(url_for('login'))