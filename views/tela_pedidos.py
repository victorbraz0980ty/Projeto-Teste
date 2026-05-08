import customtkinter as ctk
from tkinter import messagebox
from controllers.pedidos_controller import PedidoController

def renderizar_pedidos(main_frame, root, cores):
    ctrl = PedidoController(root.conn)

    for widget in main_frame.winfo_children(): widget.destroy()

    ctk.CTkLabel(main_frame, text="Pedidos 📋", font=("Arial", 24, "bold")).pack(pady=20)

    def abrir_formulario_pedido(dados_pedido=None):
        janela = ctk.CTkToplevel(root)
        janela.geometry("450x600")
        janela.attributes("-topmost", True)
        
        # Busca dados para os ComboBox via Controller
        dic_clientes, dic_produtos = ctrl.buscar_dados_auxiliares()

        ctk.CTkLabel(janela, text="Cliente:").pack(pady=5)
        combo_cli = ctk.CTkComboBox(janela, values=list(dic_clientes.keys()), width=300)
        combo_cli.pack()

        ctk.CTkLabel(janela, text="Produto:").pack(pady=5)
        combo_prod = ctk.CTkComboBox(janela, values=list(dic_produtos.keys()), width=300)
        combo_prod.pack()

        ctk.CTkLabel(janela, text="Quantidade:").pack(pady=5)
        ent_qtd = ctk.CTkEntry(janela, width=300)
        ent_qtd.insert(0, "1")
        ent_qtd.pack()

        combo_status = ctk.CTkComboBox(janela, values=['Em preparo', 'Saiu para entrega', 'Entregue'], width=300)
        combo_status.pack(pady=10)

        if dados_pedido:
            combo_cli.set(dados_pedido['nome_cliente'])
            combo_prod.set(dados_pedido['nome_produto'])
            ent_qtd.delete(0, 'end')
            ent_qtd.insert(0, str(dados_pedido['quantidade']))
            combo_status.set(dados_pedido['status_pedido'])

        def salvar():
            try:
                id_c = dic_clientes[combo_cli.get()]
                id_pr, preco = dic_produtos[combo_prod.get()]
                
                if ctrl.salvar(id_c, id_pr, ent_qtd.get(), preco, combo_status.get(), 
                               dados_pedido['id_pedidos'] if dados_pedido else None):
                    janela.destroy()
                    renderizar_pedidos(main_frame, root, cores)
                else:
                    messagebox.showerror("Erro", "Erro ao salvar pedido")
            except:
                messagebox.showerror("Erro", "Selecione opções válidas!")

        ctk.CTkButton(janela, text="Salvar", fg_color=cores['botao'], command=salvar).pack(pady=20)

    ctk.CTkButton(main_frame, text="+ Novo Pedido", fg_color=cores['botao'], command=lambda: abrir_formulario_pedido()).pack(pady=10)
    
    frame_rolagem = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
    frame_rolagem.pack(fill="both", expand=True)

    for ped in ctrl.listar():
        card = ctk.CTkFrame(frame_rolagem, fg_color="white", corner_radius=10)
        card.pack(fill="x", pady=5, padx=10)
        
        info = f"#{ped['id_pedidos']} | {ped['nome_cliente']}\n{ped['nome_produto']} (x{ped['quantidade']})"
        ctk.CTkLabel(card, text=info, font=("Arial", 12, "bold"), justify="left", text_color="black").pack(side="left", padx=20)
        
        ctk.CTkButton(card, text="Excluir", fg_color=cores['excluir'], width=60, 
                      command=lambda id_p=ped['id_pedidos']: acao_excluir(id_p)).pack(side="right", padx=10)
        
        ctk.CTkButton(card, text="Editar", fg_color=cores['editar'], width=60, 
                      command=lambda d=ped: abrir_formulario_pedido(d)).pack(side="right", padx=5)
        
        ctk.CTkLabel(card, text=f"R$ {ped['valor_total']:.2f}", font=("Arial", 12, "bold"), text_color="green").pack(side="right", padx=15)

    def acao_excluir(id_p):
        if messagebox.askyesno("Confirmar", "Excluir pedido?"):
            cursor = root.conn.cursor()
            cursor.execute("DELETE FROM itens_pedidos WHERE id_pedido=%s", (id_p,))
            cursor.execute("DELETE FROM pedidos WHERE id_pedidos=%s", (id_p,))
            root.conn.commit()
            renderizar_pedidos(main_frame, root, cores)
