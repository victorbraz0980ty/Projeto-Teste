from models.cliente_model import ClienteModel

class ClienteController:
    def __init__(self, conexao):
        self.modelo = ClienteModel(conexao)

    def listar_clientes(self):
        return self.modelo.buscar_todos()

    def validar_e_salvar(self, nome, tel_raw, cpf_raw, id_c=None):
        # Limpa os caracteres da máscara
        tel = ''.join(filter(str.isdigit, tel_raw))
        cpf = ''.join(filter(str.isdigit, cpf_raw))

        if not nome: return False, "Nome é obrigatório"
        if len(cpf) != 11: return False, "CPF deve ter 11 dígitos"
        
        try:
            self.modelo.salvar_dados(nome, tel, cpf, id_c)
            return True, "Sucesso"
        except Exception as e:
            return False, f"Erro no banco: {str(e)}"
