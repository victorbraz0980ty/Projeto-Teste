class ClienteSQL:
    def __init__(self, conexao):
        self.conn = conexao

    def buscar_todos(self):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cliente ORDER BY nome ASC")
        res = cursor.fetchall()
        cursor.close()
        return res

    def salvar_dados(self, nome, telefone, cpf, id_c=None):
        cursor = self.conn.cursor()
        if id_c:
            sql = "UPDATE cliente SET nome=%s, telefone=%s, cpf=%s WHERE id_cliente=%s"
            cursor.execute(sql, (nome, telefone, cpf, id_c))
        else:
            sql = "INSERT INTO cliente (nome, telefone, cep, endereco, cpf) VALUES (%s,%s,'0','0',%s)"
            cursor.execute(sql, (nome, telefone, cpf))
        self.conn.commit()
        cursor.close()
