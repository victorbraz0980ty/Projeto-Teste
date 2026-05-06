import customtkinter as ctk
from tkinter import messagebox
# Importa o Controller com o nome da Classe diferente do arquivo para evitar conflito
from controllers.produto_controller import ProdutoRegras

def renderizar_produtos(main_frame, root, cores):
    # Instancia o controlador (que gerencia o ProdutoModel internamente)
    ctrl = ProdutoRegras(root.conn)

    # Função idêntica à sua 'limpar_main', mas focada no frame recebido
    for widget in main_frame.winfo_children(): 
        widget.destroy()

    ctk.CTkLabel(main_frame, text="Produtos 🍕", font=("Arial", 24, "bold")).pack(pady=20)

    def abrir_formulario_produto(dados_produto=None):
        janela_formulario = ctk.CTkToplevel(root)
        janela_formulario.geometry("400x400")
        janela_formulario.attributes("-topmost", True)

        entrada_nome = ctk.CTkEntry(janela_formulario, placeholder_text="Nome", width=300)
        entrada_nome.pack(pady=10)

        entrada_preco = ctk.CTkEntry(janela_formulario, placeholder_text="Preço", width=300)
        entrada_preco.pack(pady=10)

        if dados_produto:
            entrada_nome.insert(0, dados_produto['nome_produto'])
            entrada_preco.insert(0, str(dados_produto['preco']))

        def salvar_produto():
            nome = entrada_nome.get()
            preco_txt = entrada_preco.get()
            id_p = dados_produto['id_produto'] if dados_produto else None
            
            # Chama a lógica do Controller (que faz o replace da vírgula e salva no banco)
            sucesso, erro = ctrl.validar_e_salvar(nome, preco_txt, id_p)
            
            if sucesso:
                janela_formulario.destroy()
                renderizar_produtos(main_frame, root, cores) # Recarrega a própria tela
            else:
                messagebox.showerror("Erro", erro)

        ctk.CTkButton(janela_formulario, text="Salvar", fg_color=cores['botao'], command=salvar_produto).pack(pady=20)

    # Botão de Novo Produto (estilo original)
    ctk.CTkButton(main_frame, text="+ Novo Produto", fg_color=cores['botao'], 
                  command=lambda: abrir_formulario_produto()).pack(pady=10)

    frame_rolagem = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
    frame_rolagem.pack(fill="both", expand=True)

    # Busca a lista de produtos através do Controller
    lista_produtos = ctrl.listar_para_view()

    for produto in lista_produtos:
        card_produto = ctk.CTkFrame(frame_rolagem, fg_color="white", corner_radius=10)
        card_produto.pack(fill="x", pady=5, padx=10)

        ctk.CTkLabel(card_produto, text=f"{produto['nome_produto']}", font=("Arial", 13, "bold"), text_color="black").pack(side="left", padx=15)
        ctk.CTkLabel(card_produto, text=f"R$ {produto['preco']:.2f}", font=("Arial", 12), text_color="black").pack(side="left", padx=20)

        # Botão Excluir (mantendo a chamada para a função de exclusão)
        ctk.CTkButton(card_produto, text="Excluir", fg_color=cores['excluir'], width=60, 
                      command=lambda id_p=produto['id_produto']: acao_excluir(id_p)).pack(side="right", padx=10)
        
        # Botão Editar
        ctk.CTkButton(card_produto, text="Editar", fg_color=cores['editar'], width=60, 
                      command=lambda d_p=produto: abrir_formulario_produto(d_p)).pack(side="right", padx=5)

    def acao_excluir(id_p):
        if messagebox.askyesno("Confirmar", "Deseja excluir este produto?"):
            try:
                cursor = root.conn.cursor()
                cursor.execute("DELETE FROM produtos WHERE id_produto = %s", (id_p,))
                root.conn.commit()
                cursor.close()
                renderizar_produtos(main_frame, root, cores)
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível excluir: {e}")
