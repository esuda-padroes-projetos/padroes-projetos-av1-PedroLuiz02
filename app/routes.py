from app import app, login_manager
from app.db import db
from flask import render_template, jsonify, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.models import Produto, Usuario, Pedido, ItemPedido
from app.factories import PedidoFactory
from werkzeug.security import generate_password_hash, check_password_hash
import re


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
    user = Usuario.query.all()
    pedido_aberto = None
    if current_user.is_authenticated:
        pedidos_do_usuario = current_user.pedidos
        pedido_aberto = Pedido.query.filter_by(id_usuario=current_user.id_usuario, status="Em andamento").first()
        print(f"Usuário logado: {current_user.nome}, Pedido aberto: {pedido_aberto}")
    if pedido_aberto:
        print("Itens do pedido:")
        for item in pedido_aberto.itens:
            print(f"- Produto: {item.produto.nome}, Quantidade: {item.quantidade}")
    return render_template('shop.html', produtos=produtos, user=user, pedido_aberto=pedido_aberto)


@app.context_processor
def inject_pedido_aberto():
    if current_user.is_authenticated:
        pedido_aberto = next((p for p in current_user.pedidos if p.status == "Em andamento"), None)
    else:
        pedido_aberto = None
    return dict(pedido_aberto=pedido_aberto)


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
    origem = request.referrer or url_for("shop")

    pedido = Pedido.query.filter_by(id_usuario=usuario.id_usuario, status="Em andamento").first()

    if not pedido:
        pedido = Pedido(id_usuario=usuario.id_usuario, status="Em andamento")
        db.session.add(pedido)
        db.session.flush()

    for produto_id, qtd in zip(produto_ids, quantidades):
        produto = Produto.query.get(int(produto_id))
        if not produto:
            continue

        item_existente = ItemPedido.query.filter_by(id_pedido=pedido.id_pedido, id_produto=produto.id_produto).first()

        if item_existente:
            item_existente.quantidade += int(qtd)
        else:
            novo_item = ItemPedido(
                id_pedido=pedido.id_pedido,
                id_produto=produto.id_produto,
                quantidade=int(qtd)
            )
            db.session.add(novo_item)

    db.session.commit()
    return redirect(origem)


@app.route("/sobre")
def contato():
    return render_template('sobre.html')



@app.route("/item/deletar/<int:id_item>", methods=["POST"])
@login_required
def deletar_item_route(id_item):
    origem = request.referrer or url_for("shop")

    item = ItemPedido.query.get(id_item)
    if item and item.pedido.id_usuario == current_user.id_usuario:
        db.session.delete(item)
        db.session.commit()
        print("Item removido com sucesso!", "success")
    else:
        print("Item não encontrado ou não pertence ao seu pedido!", "danger")
    if not item.pedido.itens:
        db.session.delete(item.pedido)
        db.session.commit()
        print("Pedido removido porque ficou vazio.", "info")
    return redirect(origem)


regex_nome = r"^[A-Za-zÀ-ÖØ-öø-ÿ]+(?: [A-Za-zÀ-ÖØ-öø-ÿ]+)+$"
regex_senha = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&._-])[A-Za-z\d@$!%*?&._-]{6,}$"
regex_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['emailForm']
        senha = request.form['senhaForm']

        user = db.session.query(Usuario).filter_by(email=email).first()
        if not user or not check_password_hash(user.senha, senha):
            flash("Email ou senha incorretos.", "error")
            return redirect(url_for('login'))
        
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

        if not re.match(regex_nome, nome):
            flash("Nome não adequado, tente novamente.", "error")
            return redirect(url_for('register'))
        
        if not re.match(regex_email, email):
            flash("E-mail inválido, tente novamente.", "error")
            return redirect(url_for('register'))
        
        if senha != confirm_senha:
            flash("As senhas não coincidem.", "error")
            return redirect(url_for('register'))

        if not re.match(regex_senha, senha):
            flash("A senha deve ter pelo menos 6 caracteres, incluindo letra maiúscula, minúscula, número e símbolo.", "error")
            return redirect(url_for('register'))

        senha_hash = generate_password_hash(senha)

        novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()

        login_user(novo_usuario)

        flash("Usuário registrado com sucesso!", "success")
        return redirect(url_for('login'))
    

"""
Nome Completo: Pelo menos Nome e Sobrenome
Email: após o @, domínio do e-mail (gmail ou outlook) e extensão do domínio (.com ou .br)
Senha: Precisa conter 1 caractere minúscula, 1 caractere maiúscula, 1 número e 1 caractere especial
"""
    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))