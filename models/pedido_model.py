class PedidoSQL:
    def __init__(self, conexao):
        self.conn = conexao

    def listar_pedidos_completos(self):
        cursor = self.conn.cursor(dictionary=True)
        sql = """
            SELECT p.*, c.nome as nome_cliente, pr.nome_produto, i.quantidade, 
            DATE_FORMAT(p.data_hora, '%%d/%%m %%H:%%i') as data_formatada 
            FROM pedidos p 
            JOIN cliente c ON p.id_cliente = c.id_cliente 
            JOIN itens_pedidos i ON p.id_pedidos = i.id_pedido 
            JOIN produtos pr ON i.id_produto = pr.id_produto 
            ORDER BY p.id_pedidos DESC
        """
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        return res

    def salvar_pedido_completo(self, id_cliente, id_produto, qtd, preco_unit, status, id_p=None):
        cursor = self.conn.cursor()
        valor_total = float(preco_unit) * int(qtd)

        if id_p:
            # Atualiza Pedido
            cursor.execute("UPDATE pedidos SET id_cliente=%s, valor_total=%s, status_pedido=%s WHERE id_pedidos=%s",
                           (id_cliente, valor_total, status, id_p))
            # Atualiza Item
            cursor.execute("UPDATE itens_pedidos SET id_produto=%s, quantidade=%s WHERE id_pedido=%s",
                           (id_produto, qtd, id_p))
        else:
            # Insere Novo Pedido
            cursor.execute("INSERT INTO pedidos (id_cliente, valor_total, status_pedido, data_hora) VALUES (%s,%s,%s,NOW())",
                           (id_cliente, valor_total, status))
            id_novo = cursor.lastrowid
            # Insere Item
            cursor.execute("INSERT INTO itens_pedidos (id_pedido, id_produto, quantidade) VALUES (%s,%s,%s)",
                           (id_novo, id_produto, qtd))
        
        self.conn.commit()
        cursor.close()
