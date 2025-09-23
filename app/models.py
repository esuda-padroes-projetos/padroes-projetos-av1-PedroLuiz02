from app.db import db
from flask_login import UserMixin
from sqlalchemy import ForeignKey, Numeric, func, Enum
from sqlalchemy.orm import relationship


class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

    pedidos = db.relationship("Pedido", back_populates="usuario")

    def get_id(self):
        return str(self.id_usuario)

class Produto(db.Model):
    __tablename__ = "produtos"

    id_produto = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String())
    preco_unitario = db.Column(Numeric(10, 2), nullable=False)
    sabor = db.Column(db.String(50), nullable=False)
    imagem = db.Column(db.String(200), nullable=False)

    pacotes = relationship("Pacote", back_populates="produto")


class Pacote(db.Model):
    __tablename__ = "pacotes"

    id_pacote = db.Column(db.Integer, primary_key=True)
    id_produto = db.Column(db.Integer, ForeignKey("produtos.id_produto"), nullable=False)
    quantidade = db.Column(db.Integer, default=5)
    preco_pacote = db.Column(Numeric(10, 2), nullable=False)

    produto = relationship("Produto", back_populates="pacotes")

class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id_pedido = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    data_pedido = db.Column(db.DateTime, server_default=func.now())
    status = db.Column(db.String(20), default="Em andamento")

    usuario = db.relationship("Usuario", back_populates="pedidos")
    itens = db.relationship("ItemPedido", back_populates="pedido")

class ItemPedido(db.Model):
    __tablename__ = 'itens_pedidos'

    id_item = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey("pedidos.id_pedido"), nullable=False)
    id_produto = db.Column(db.Integer, db.ForeignKey("produtos.id_produto"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

    pedido = db.relationship("Pedido", back_populates="itens")
    produto = db.relationship("Produto")
