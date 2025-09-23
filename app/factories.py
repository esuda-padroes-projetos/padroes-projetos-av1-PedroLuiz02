from app.models import Pedido, ItemPedido

class PedidoFactory:
    @staticmethod
    def criar_pedido(usuario, itens, status="Em andamento"):
        pedido = Pedido(usuario=usuario, status=status)
        for produto, qtd in itens:
            item = ItemPedido(produto=produto, quantidade=qtd)
            pedido.itens.append(item)
        return pedido