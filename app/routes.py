from app import app, login_manager
from app.db import db
from flask import render_template, jsonify, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.models import Produto, Usuario, Pedido, ItemPedido
from app.factories import PedidoFactory
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


@app.route('/shop')
def shop():
    produtos = Produto.query.all()
    if current_user.is_authenticated:
        print(current_user.nome)
    return render_template('shop.html', produtos=produtos)


@app.route('/product/<int:id>')
def product(id):
    produto = Produto.query.get_or_404(id)
    if current_user.is_authenticated:
        print(current_user.nome)
    return render_template('product.html', produto=produto)


@app.route("/criar_pedido", methods=["POST"])
@login_required
def criar_pedido():
    usuario = current_user
    produto_ids = request.form.getlist("produto_id[]")
    quantidades = request.form.getlist("quantidade[]")

    itens = []
    for produto_id, qtd in zip(produto_ids, quantidades):
        produto = Produto.query.get(int(produto_id))
        if produto:
            itens.append((produto, int(qtd)))

    if not itens:
        return redirect(url_for("shop"))

    pedido = PedidoFactory.criar_pedido(usuario, itens)

    db.session.add(pedido)
    db.session.commit()

    return redirect(url_for("shop"))


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
    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

