import customtkinter as ctk
from controllers.dashboard_controller import DashboardRegras

def renderizar_dashboard(main_frame, root, cores):
    ctrl = DashboardRegras(root.conn)
    dados = ctrl.pegar_dados_resumo()

    # Limpar tela
    for widget in main_frame.winfo_children(): 
        widget.destroy()

    ctk.CTkLabel(main_frame, text="Dashboard Pizzaloop 🍕", font=("Arial", 30, "bold")).pack(pady=30)

    # Container para os cards
    frame_cards = ctk.CTkFrame(main_frame, fg_color="transparent")
    frame_cards.pack(fill="x", padx=50)

    def criar_card(titulo, valor, cor_barra):
        card = ctk.CTkFrame(frame_cards, width=250, height=150, corner_radius=15, fg_color="white")
        card.pack(side="left", padx=20, pady=20, expand=True)
        card.pack_propagate(False)

        # Barrinha colorida no topo do card
        barra = ctk.CTkFrame(card, height=10, fg_color=cor_barra, corner_radius=0)
        barra.pack(fill="x", side="top")

        ctk.CTkLabel(card, text=titulo, font=("Arial", 16), text_color="gray").pack(pady=(20, 5))
        ctk.CTkLabel(card, text=valor, font=("Arial", 28, "bold"), text_color="black").pack()

    # Criando os 3 cards principais
    criar_card("Total Clientes", dados["clientes"], "#3498db")
    criar_card("Pedidos Realizados", dados["pedidos"], cores["botao"])
    criar_card("Faturamento Total", dados["faturamento"], "#2ecc71")

    # Mensagem de boas-vindas ou log
    ctk.CTkLabel(main_frame, text="Sistema operando normalmente ✅", 
                 font=("Arial", 12), text_color="gray").pack(side="bottom", pady=20)
