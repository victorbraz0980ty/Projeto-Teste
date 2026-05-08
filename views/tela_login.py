import customtkinter as ctk
from tkinter import messagebox
from controllers.login_controller import LoginController

def renderizar_login(root, callback_sucesso):
    # root aqui é a janela login_win instanciada no main
    regras = LoginController(root.conn)

    # Cores fixas do seu design
    DARK, ORANGE, LIGHT_BG = "#0d1b2a", "#ff6b00", "#f5f6f8"

    # Painel Lateral
    frame_lateral = ctk.CTkFrame(root, width=350, fg_color=DARK, corner_radius=0)
    frame_lateral.pack(side="left", fill="y")
    ctk.CTkLabel(frame_lateral, text="🍕 Pizzaloop", font=("Arial", 24, "bold"), text_color="white").place(relx=0.5, rely=0.4, anchor="center")

    # Painel Direito
    frame_principal = ctk.CTkFrame(root, fg_color=LIGHT_BG, corner_radius=0)
    frame_principal.pack(side="right", fill="both", expand=True)

    # Card Central
    card = ctk.CTkFrame(frame_principal, width=350, height=400, corner_radius=15, fg_color="white")
    card.place(relx=0.5, rely=0.5, anchor="center")

    ent_email = ctk.CTkEntry(card, placeholder_text="Email", width=260)
    ent_email.pack(pady=(50, 10))

    ent_senha = ctk.CTkEntry(card, placeholder_text="Senha", show="*", width=260)
    ent_senha.pack(pady=10)

    def tentar_entrar():
        sucesso, msg = regras.autenticar(ent_email.get(), ent_senha.get())
        if sucesso:
            callback_sucesso() # Função no main que fecha login e abre sistema
        else:
            messagebox.showerror("Erro", msg)

    ctk.CTkButton(card, text="Entrar", fg_color=ORANGE, command=tentar_entrar).pack(pady=20)

    def abrir_cadastro():
        janela_cad = ctk.CTkToplevel(root)
        janela_cad.geometry("400x400")
        janela_cad.attributes("-topmost", True)
        
        e_mail = ctk.CTkEntry(janela_cad, placeholder_text="Novo Email", width=300)
        e_mail.pack(pady=20)
        p_pass = ctk.CTkEntry(janela_cad, placeholder_text="Nova Senha", show="*", width=300)
        p_pass.pack(pady=10)

        def salvar():
            ok, m = regras.cadastrar_novo(e_mail.get(), p_pass.get())
            if ok: 
                messagebox.showinfo("Sucesso", m)
                janela_cad.destroy()
            else: 
                messagebox.showerror("Erro", m)

        ctk.CTkButton(janela_cad, text="Cadastrar", fg_color=ORANGE, command=salvar).pack(pady=20)

    link = ctk.CTkLabel(card, text="Criar conta", cursor="hand2", text_color="gray")
    link.pack()
    link.bind("<Button-1>", lambda e: abrir_cadastro())
