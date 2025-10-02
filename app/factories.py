from app.models import Pedido, ItemPedido

class PedidoFactory:
    @staticmethod
    def criar_pedido(usuario, itens, status="Em andamento"):
        pedido = Pedido(id_usuario=usuario.id_usuario, status=status)
        
        for produto, qtd in itens:
            item = ItemPedido(
                quantidade=qtd,
                produto=produto,
                pedido=pedido
            )
            pedido.itens.append(item)

        print([ (i.produto.nome, i.quantidade, i.pedido) for i in pedido.itens ])
        print(f"Pedido {pedido.id_pedido} com {len(pedido.itens)} itens")
        for i in pedido.itens:
            print(f"- {i.produto.nome} x {i.quantidade}")
        return pedido
