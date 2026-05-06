import customtkinter as ctk
from tkinter import messagebox
from controllers.cliente_controller import ClienteRegras

# IMPORTANTE: Importar todas as funções necessárias da pasta utils
from utils.formatadores import (
    aplicar_mascara_tel, 
    aplicar_mascara_cpf, 
    formatar_cpf, 
    formatar_telefone
)

def renderizar_clientes(main_frame, root, cores):
    # Instancia o controlador
    ctrl = ClienteRegras(root.conn)

    # Limpa o frame principal antes de desenhar
    for widget in main_frame.winfo_children(): 
        widget.destroy()

    ctk.CTkLabel(main_frame, text="Gerenciar Clientes 👥", font=("Arial", 24, "bold")).pack(pady=20)

    def abrir_formulario(dados_cliente=None):
        janela = ctk.CTkToplevel(root)
        janela.geometry("400x480")
        janela.attributes("-topmost", True)
        janela.title("Cliente")

        ent_nome = ctk.CTkEntry(janela, placeholder_text="Nome", width=300)
        ent_nome.pack(pady=10)

        ent_tel = ctk.CTkEntry(janela, placeholder_text="(00) 00000-0000", width=300)
        ent_tel.pack(pady=10)
        ent_tel.bind("<KeyRelease>", aplicar_mascara_tel) # Máscara ativa

        ent_cpf = ctk.CTkEntry(janela, placeholder_text="000.000.000-00", width=300)
        ent_cpf.pack(pady=10)
        ent_cpf.bind("<KeyRelease>", aplicar_mascara_cpf) # Máscara ativa

        # Se for edição, preenche os campos
        if dados_cliente:
            ent_nome.insert(0, dados_cliente['nome'])
            ent_tel.insert(0, formatar_telefone(dados_cliente['telefone']))
            ent_cpf.insert(0, formatar_cpf(dados_cliente['cpf']))

        def salvar():
            sucesso, erro = ctrl.validar_e_salvar(
                ent_nome.get(), 
                ent_tel.get(), 
                ent_cpf.get(), 
                dados_cliente['id_cliente'] if dados_cliente else None
            )
            if sucesso:
                janela.destroy()
                renderizar_clientes(main_frame, root, cores) # Recarrega a tela
            else:
                messagebox.showerror("Erro", erro)

        ctk.CTkButton(janela, text="Salvar", fg_color=cores['botao'], command=salvar).pack(pady=20)

    # Botão de Novo Cliente
    ctk.CTkButton(main_frame, text="+ Novo Cliente", fg_color=cores['botao'], 
                  command=lambda: abrir_formulario()).pack(pady=10)

    # Listagem de Clientes
    frame_rolagem = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
    frame_rolagem.pack(fill="both", expand=True)

    for cliente in ctrl.listar_clientes():
        card = ctk.CTkFrame(frame_rolagem, fg_color="white", corner_radius=10)
        card.pack(fill="x", pady=5, padx=10)

        # Informações do Cliente no Card
        ctk.CTkLabel(card, text=f"{cliente['nome']}\nCPF: {formatar_cpf(cliente['cpf'])}", 
                     font=("Arial", 13, "bold"), justify="left", text_color="black").pack(side="left", padx=20, pady=10)
        
        ctk.CTkLabel(card, text=f"📞 {formatar_telefone(cliente['telefone'])}", 
                     font=("Arial", 12), text_color="gray").pack(side="left", padx=30)

        # Botões de Ação
        ctk.CTkButton(card, text="Excluir", fg_color=cores['excluir'], width=60, 
                      command=lambda id_c=cliente['id_cliente']: acao_excluir(id_c)).pack(side="right", padx=10)
        
        ctk.CTkButton(card, text="Editar", fg_color=cores['editar'], width=60, 
                      command=lambda d=cliente: abrir_formulario(d)).pack(side="right", padx=5)

    def acao_excluir(id_c):
        if messagebox.askyesno("Confirmar", "Excluir cliente?"):
            try:
                cursor = root.conn.cursor()
                cursor.execute("DELETE FROM cliente WHERE id_cliente=%s", (id_c,))
                root.conn.commit()
                cursor.close()
                renderizar_clientes(main_frame, root, cores)
            except:
                messagebox.showerror("Erro", "Cliente possui pedidos vinculados.")
