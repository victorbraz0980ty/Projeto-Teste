import customtkinter as ctk

class TelaSistema(ctk.CTk):
    def __init__(self, cores, callback_navegacao):
        super().__init__()
        
        # Configurações da Janela
        self.title("Gestão Pizzaloop")
        self.attributes("-fullscreen", True)
        self.cores = cores

        # Layout: Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color=self.cores["sidebar"])
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
            ctk.CTkButton(
                self.sidebar, text=texto, fg_color="transparent", anchor="w",
                command=lambda d=destino: callback_navegacao(d)
            ).pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(self.sidebar, text="Sair", fg_color="#333", 
                      command=self.quit).pack(side="bottom", pady=20, padx=20, fill="x")

        # Layout: Main Frame (Onde as outras views entram)
        self.main_frame = ctk.CTkFrame(self, fg_color=self.cores["fundo"])
        self.main_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)
