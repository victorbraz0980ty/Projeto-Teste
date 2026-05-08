from models.dashboard_model import DashboardModel

class DashboardController:
    def __init__(self, conexao):
        self.modelo = DashboardModel(conexao)

    def pegar_dados_resumo(self):
        clientes, pedidos, grana = self.modelo.obter_estatisticas()
        return {
            "clientes": f"{clientes}",
            "pedidos": f"{pedidos}",
            "faturamento": f"R$ {grana:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        }
