class ProdutoModel:
    def __init__(self, conexao):
        self.conn = conexao

    def buscar_todos(self):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM produtos")
        res = cursor.fetchall()
        cursor.close()
        return res

    def salvar_dados(self, nome, preco, id_p=None):
        cursor = self.conn.cursor()
        if id_p:
            cursor.execute("UPDATE produtos SET nome_produto=%s, preco=%s WHERE id_produto=%s", (nome, preco, id_p))
        else:
            cursor.execute("INSERT INTO produtos (nome_produto, preco, categoria) VALUES (%s,%s,'Pizza')", (nome, preco))
        self.conn.commit()
        cursor.close()
