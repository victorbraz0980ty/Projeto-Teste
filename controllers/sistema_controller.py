import customtkinter as ctk
from banco.connect import connect_to_database
from views.tela_sistema import TelaSistema
from views.tela_login import renderizar_login
from views.tela_dashboard import renderizar_dashboard
from views.tela_produtos import renderizar_produtos
from views.tela_clientes import renderizar_clientes
from views.tela_pedidos import renderizar_pedidos

class SistemaController:
    def __init__(self):
        ctk.set_appearance_mode("light")
        self.cores = {
            "sidebar": "#1E1E2F", "fundo": "#F5F5F5", "botao": "#FF6B00",
            "editar": "#4CAF50", "excluir": "#F44336", "texto_claro": "#FFFFFF"
        }
        self.conn = connect_to_database()
        self.root = None

    def iniciar(self):
        self.login_win = ctk.CTk()
        self.login_win.title("Login - Pizzaloop")
        self.login_win.geometry("1200x600")
        self.login_win.conn = self.conn
        renderizar_login(self.login_win, self.iniciar_interface_principal)
        self.login_win.mainloop()

    def iniciar_interface_principal(self):
        if hasattr(self, 'login_win'):
            self.login_win.destroy()

        # Instancia a View que acabamos de criar
        self.root = TelaSistema(self.cores, self.mudar_tela)
        self.root.conn = self.conn # Repassa a conexão
        
        self.mudar_tela("dashboard")
        self.root.mainloop()

    def mudar_tela(self, nome_tela):
        # Limpa o frame central da view
        for widget in self.root.main_frame.winfo_children():
            widget.destroy()

        # Dicionário de roteamento para as funções prontas
        telas = {
            "dashboard": renderizar_dashboard,
            "pedidos": renderizar_pedidos,
            "clientes": renderizar_clientes,
            "produtos": renderizar_produtos
        }

        if nome_tela in telas:
            telas[nome_tela](self.root.main_frame, self.root, self.cores)
