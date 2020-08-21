class sugestaoPedido():
    def __init__(self, pedido,estoque):
        self.op = pedido.op
        self.largura = estoque.largura
        self.item = estoque.item
        self.quantidade = estoque.quantidade
        self.metros = estoque.metros
        self.endereco = estoque.endereco
        self.area = estoque.area
        self.cod_barra = estoque.cod_barra
        self.refile = ((estoque.largura - pedido.largura)*100)/estoque.largura

    def __repr__(self):
        return f'Op {self.op}'
    