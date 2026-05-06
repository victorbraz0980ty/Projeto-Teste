from models.login_model import LoginSQL

class LoginRegras:
    def __init__(self, conexao):
        self.modelo = LoginSQL(conexao)

    def autenticar(self, email, senha):
        if not email or not senha:
            return False, "Preencha todos os campos!"
        
        usuario = self.modelo.buscar_usuario(email.strip())
        
        if usuario and usuario[0] == senha.strip():
            return True, "Login realizado!"
        return False, "E-mail ou senha incorretos."

    def cadastrar_novo(self, email, senha):
        if not email or not senha:
            return False, "Preencha todos os campos!"
        try:
            self.modelo.criar_usuario(email, senha)
            return True, "Usuário cadastrado!"
        except:
            return False, "Erro: E-mail já cadastrado."
