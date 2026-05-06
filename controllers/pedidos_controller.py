from models.pedido_model import PedidoSQL

class PedidosRegras:
    def __init__(self, conexao):
        self.modelo = PedidoSQL(conexao)
        self.conn = conexao

    def buscar_dados_auxiliares(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id_cliente, nome FROM cliente")
        clientes = {nome: id_cli for id_cli, nome in cursor.fetchall()}
        
        cursor.execute("SELECT id_produto, nome_produto, preco FROM produtos")
        produtos = {nome: (id_prod, preco) for id_prod, nome, preco in cursor.fetchall()}
        cursor.close()
        return clientes, produtos

    def listar(self):
        return self.modelo.listar_pedidos_completos()

    def salvar(self, id_cli, id_prod, qtd, preco, status, id_p=None):
        try:
            self.modelo.salvar_pedido_completo(id_cli, id_prod, qtd, preco, status, id_p)
            return True
        except:
            return False
