class LoginSQL:
    def __init__(self, conexao):
        self.conn = conexao

    def buscar_usuario(self, email):
        cursor = self.conn.cursor()
        cursor.execute("SELECT senha FROM login WHERE email=%s", (email,))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado # Retorna a senha ou None
    
    def criar_usuario(self, email, senha):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO login (email, senha) VALUES (%s, %s)", (email, senha))
        self.conn.commit()
        cursor.close()