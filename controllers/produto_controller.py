from models.produto_model import ProdutoModel

class ProdutoController:
    def __init__(self, conexao):
        self.modelo = ProdutoModel(conexao)

    def listar_para_view(self):
        return self.modelo.buscar_todos()

    def validar_e_salvar(self, nome, preco_texto, id_p=None):
        try:
            if not nome: return False, "Nome obrigatório"
            preco_limpo = float(preco_texto.replace(",", "."))
            self.modelo.salvar_dados(nome, preco_limpo, id_p)
            return True, "Sucesso"
        except Exception as e:
            return False, f"Erro: {str(e)}"
