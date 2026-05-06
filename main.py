import customtkinter as ctk
from banco.connect import connect_to_database

# IMPORTAÇÃO DAS VIEWS (Nomes de arquivos e funções que definimos)
from views.tela_login import renderizar_login
from views.tela_dashboard import renderizar_dashboard
from views.tela_produtos import renderizar_produtos
from views.tela_clientes import renderizar_clientes
from views.tela_pedidos import renderizar_pedidos

class SistemaPizzaloop:
    def __init__(self):
        # 1. Configurações Globais de Design
        ctk.set_appearance_mode("light")
        self.cores = {
            "sidebar": "#1E1E2F",
            "fundo": "#F5F5F5",
            "botao": "#FF6B00",
            "editar": "#4CAF50",
            "excluir": "#F44336",
            "texto_claro": "#FFFFFF"
        }

        # 2. Conexão com o Banco (Inicia uma vez e repassa para as telas)
        try:
            self.conn = connect_to_database()
        except Exception as e:
            print(f"Erro fatal de conexão: {e}")
            return

        # 3. Inicia pelo Login
        self.abrir_janela_login()

    def abrir_janela_login(self):
        self.login_win = ctk.CTk()
        self.login_win.title("Login - Pizzaloop")
        self.login_win.geometry("1200x600")
        self.login_win.conn = self.conn # Injeta a conexão na janela de login

        # Chama a view de login e passa a função 'iniciar_sistema' como retorno de sucesso
        renderizar_login(self.login_win, self.iniciar_sistema)
        self.login_win.mainloop()

    def iniciar_sistema(self):
        # Fecha o login e abre a interface principal
        if hasattr(self, 'login_win'):
            self.login_win.destroy()

        self.root = ctk.CTk()
        self.root.title("Gestão Pizzaloop")
        self.root.attributes("-fullscreen", True)
        self.root.conn = self.conn # Mantém a conexão ativa

        # Layout: Sidebar
        self.sidebar = ctk.CTkFrame(self.root, width=200, corner_radius=0, fg_color=self.cores["sidebar"])
        self.sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(self.sidebar, text="Pizzaloop", font=("Arial", 22, "bold"), 
                     text_color=self.cores["texto_claro"]).pack(pady=30)

        # Botões de Navegação
        botoes = [
            ("Dashboard", "dashboard"),
            ("Pedidos", "pedidos"),
            ("Clientes", "clientes"),
            ("Produtos", "produtos")
        ]

        for texto, destino in botoes:
            ctk.CTkButton(self.sidebar, text=texto, fg_color="transparent", anchor="w",
                          command=lambda d=destino: self.mudar_tela(d)).pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(self.sidebar, text="Sair", fg_color="#333", 
                      command=self.root.quit).pack(side="bottom", pady=20, padx=20, fill="x")

        # Layout: Main Frame (Container das telas)
        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.cores["fundo"])
        self.main_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # Inicia na Dashboard
        self.mudar_tela("dashboard")
        self.root.mainloop()

    def mudar_tela(self, nome_tela):
        # Limpar o frame atual antes de carregar a nova view (idêntico ao seu limpar_main)
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Roteamento das telas
        if nome_tela == "dashboard":
            renderizar_dashboard(self.main_frame, self.root, self.cores)
        elif nome_tela == "pedidos":
            renderizar_pedidos(self.main_frame, self.root, self.cores)
        elif nome_tela == "clientes":
            renderizar_clientes(self.main_frame, self.root, self.cores)
        elif nome_tela == "produtos":
            renderizar_produtos(self.main_frame, self.root, self.cores)

if __name__ == "__main__":
    SistemaPizzaloop()
