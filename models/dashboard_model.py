class DashboardModel:
    def __init__(self, conexao):
        self.conn = conexao

    def obter_estatisticas(self):
        cursor = self.conn.cursor()
        
        # Total de Clientes
        cursor.execute("SELECT COUNT(*) FROM cliente")
        total_clientes = cursor.fetchone()[0]
        
        # Total de Pedidos
        cursor.execute("SELECT COUNT(*) FROM pedidos")
        total_pedidos = cursor.fetchone()[0]
        
        # Faturamento Total
        cursor.execute("SELECT SUM(valor_total) FROM pedidos")
        faturamento = cursor.fetchone()[0] or 0.0
        
        cursor.close()
        return total_clientes, total_pedidos, faturamento
