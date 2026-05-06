'''
import mysql.connector
import customtkinter as ctk
from tkinter import messagebox
from banco.connect import connect_to_database

# =======================
# CONFIGURAÇÕES DE DESIGN
# =======================
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

COR_SIDEBAR, COR_TEXTO, COR_FUNDO = "#1E1E2F", "#FFFFFF", "#F5F5F5"
COR_BOTAO, COR_EDITAR, COR_EXCLUIR = "#FF6B00", "#4CAF50", "#F44336"
ORANGE, DARK, LIGHT_BG = "#ff6b00", "#0d1b2a", "#f5f6f8"

# =======================
# FUNÇÕES DE FORMATAÇÃO E MÁSCARAS
# =======================
def aplicar_mascara_cpf(evento):
    # Obtém apenas os números digitados
    texto_numerico = ''.join(filter(str.isdigit, evento.widget.get()))
    cpf_formatado = ""
    
    for indice, caractere in enumerate(texto_numerico):
        if indice == 3 or indice == 6: 
            cpf_formatado += "."
        elif indice == 9: 
            cpf_formatado += "-"
        cpf_formatado += caractere
        
    evento.widget.delete(0, "end")
    evento.widget.insert(0, cpf_formatado[:14])

def aplicar_mascara_tel(evento):
    # Obtém apenas os números digitados
    texto_numerico = ''.join(filter(str.isdigit, evento.widget.get()))
    tel_formatado = ""
    
    for indice, caractere in enumerate(texto_numerico):
        if indice == 0: 
            tel_formatado += "("
        elif indice == 2: 
            tel_formatado += ") "
        elif indice == 7: 
            tel_formatado += "-"
        tel_formatado += caractere
        
    evento.widget.delete(0, "end")
    evento.widget.insert(0, tel_formatado[:15])

def formatar_cpf(valor_cpf):
    numeros = ''.join(filter(str.isdigit, str(valor_cpf)))
    if len(numeros) == 11:
        return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"
    return numeros

def formatar_telefone(valor_tel):
    numeros = ''.join(filter(str.isdigit, str(valor_tel)))
    if len(numeros) == 11: 
        return f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:]}"
    elif len(numeros) == 10: 
        return f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}"
    return numeros


# =======================
# TELA DO SISTEMA
# =======================
def iniciar_sistema():
    global root, main_frame
    
    root = ctk.CTk()
    root.title("Gestão Pizzaloop")
    root.geometry("1200x800")
    root.attributes("-fullscreen", True)
    root.conn = connect_to_database()

    sidebar = ctk.CTkFrame(root, width=200, corner_radius=0, fg_color=COR_SIDEBAR)
    sidebar.pack(side="left", fill="y")
    ctk.CTkLabel(sidebar, text="Pizzaloop", font=("Arial", 22, "bold"), text_color=COR_TEXTO).pack(pady=30)

    main_frame = ctk.CTkFrame(root, fg_color=COR_FUNDO)
    main_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    ctk.CTkButton(sidebar, text="Dashboard", command=tela_dashboard).pack(pady=15, padx=20)
    ctk.CTkButton(sidebar, text="Pedidos", command=tela_pedidos).pack(pady=15, padx=20)
    ctk.CTkButton(sidebar, text="Clientes", command=tela_clientes).pack(pady=15, padx=20)
    ctk.CTkButton(sidebar, text="Produtos", command=tela_produtos).pack(pady=15, padx=20)
    ctk.CTkButton(sidebar, text="Sair", fg_color="#333", command=root.quit).pack(side="bottom", pady=20)

    tela_dashboard()
    root.mainloop()

def limpar_main():
    for widget in main_frame.winfo_children(): widget.destroy()

def tela_dashboard():
    limpar_main()
    ctk.CTkLabel(main_frame, text="Dashboard Pizzaloop 🍕", font=("Arial", 30, "bold")).pack(pady=50)

# =======================
# TELA DE CLIENTES
# =======================

def tela_clientes():
    limpar_main()
    ctk.CTkLabel(main_frame, text="Gerenciar Clientes 👥", font=("Arial", 24, "bold")).pack(pady=20)

    def abrir_formulario(dados_cliente=None):
        janela_formulario = ctk.CTkToplevel(root)
        janela_formulario.geometry("400x480")
        janela_formulario.attributes("-topmost", True)

        entrada_nome = ctk.CTkEntry(janela_formulario, placeholder_text="Nome", width=300)
        entrada_nome.pack(pady=10)

        entrada_telefone = ctk.CTkEntry(janela_formulario, placeholder_text="(00) 00000-0000", width=300)
        entrada_telefone.pack(pady=10)
        entrada_telefone.bind("<KeyRelease>", aplicar_mascara_tel)

        entrada_cpf = ctk.CTkEntry(janela_formulario, placeholder_text="000.000.000-00", width=300)
        entrada_cpf.pack(pady=10)
        entrada_cpf.bind("<KeyRelease>", aplicar_mascara_cpf)

        if dados_cliente:
            entrada_nome.insert(0, dados_cliente['nome'])
            entrada_telefone.insert(0, formatar_telefone(dados_cliente['telefone']))
            entrada_cpf.insert(0, formatar_cpf(dados_cliente['cpf']))

        def salvar_dados():
            nome = entrada_nome.get()
            telefone = ''.join(filter(str.isdigit, entrada_telefone.get()))
            cpf = ''.join(filter(str.isdigit, entrada_cpf.get()))

            if len(cpf) != 11:
                messagebox.showerror("Erro", "CPF Inválido")
                return

            try:
                cursor_db = root.conn.cursor()
                if dados_cliente:
                    consulta_atualizar = "UPDATE cliente SET nome=%s, telefone=%s, cpf=%s WHERE id_cliente=%s"
                    cursor_db.execute(consulta_atualizar, (nome, telefone, cpf, dados_cliente['id_cliente']))
                else:
                    consulta_inserir = "INSERT INTO cliente (nome, telefone, cep, endereco, cpf) VALUES (%s,%s,'0','0',%s)"
                    cursor_db.execute(consulta_inserir, (nome, telefone, cpf))
                
                root.conn.commit()
                cursor_db.close()
                janela_formulario.destroy()
                tela_clientes()
            except Exception as erro:
                messagebox.showerror("Erro", str(erro))

        ctk.CTkButton(janela_formulario, text="Salvar", fg_color=COR_BOTAO, command=salvar_dados).pack(pady=20)

    ctk.CTkButton(main_frame, text="+ Novo Cliente", fg_color=COR_BOTAO, command=lambda: abrir_formulario()).pack(pady=10)

    frame_rolagem = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
    frame_rolagem.pack(fill="both", expand=True)

    cursor_lista = root.conn.cursor(dictionary=True)
    consulta_listar = "SELECT * FROM cliente ORDER BY nome ASC"
    cursor_lista.execute(consulta_listar)

    for cliente in cursor_lista.fetchall():
        frame_cliente = ctk.CTkFrame(frame_rolagem, fg_color="white", corner_radius=10)
        frame_cliente.pack(fill="x", pady=5, padx=10)

        ctk.CTkLabel(frame_cliente, text=f"{cliente['nome']}\nCPF: {formatar_cpf(cliente['cpf'])}", 
                     font=("Arial", 13, "bold"), justify="left").pack(side="left", padx=20, pady=10)
        
        ctk.CTkLabel(frame_cliente, text=f"📞 {formatar_telefone(cliente['telefone'])}", 
                     font=("Arial", 12), text_color="gray").pack(side="left", padx=30)

        ctk.CTkButton(frame_cliente, text="Excluir", fg_color=COR_EXCLUIR, width=60, 
                      command=lambda id_c=cliente['id_cliente']: excluir_item(id_c, "cliente")).pack(side="right", padx=10)
        
        ctk.CTkButton(frame_cliente, text="Editar", fg_color=COR_EDITAR, width=60, 
                      command=lambda d=cliente: abrir_formulario(d)).pack(side="right", padx=5)
    
    cursor_lista.close()

# =======================
# TELA DE PRODUTOS
# =======================

def tela_produtos():
    limpar_main()
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
            try:
                cursor_db = root.conn.cursor()
                nome = entrada_nome.get()
                preco = float(entrada_preco.get().replace(",", "."))

                if dados_produto:
                    consulta_atualizar = "UPDATE produtos SET nome_produto=%s, preco=%s WHERE id_produto=%s"
                    cursor_db.execute(consulta_atualizar, (nome, preco, dados_produto['id_produto']))
                else:
                    consulta_inserir = "INSERT INTO produtos (nome_produto, preco, categoria) VALUES (%s,%s,'Pizza')"
                    cursor_db.execute(consulta_inserir, (nome, preco))

                root.conn.commit()
                cursor_db.close()
                janela_formulario.destroy()
                tela_produtos()
            except Exception as erro:
                messagebox.showerror("Erro", str(erro))

        ctk.CTkButton(janela_formulario, text="Salvar", fg_color=COR_BOTAO, command=salvar_produto).pack(pady=20)

    ctk.CTkButton(main_frame, text="+ Novo Produto", fg_color=COR_BOTAO, command=lambda: abrir_formulario_produto()).pack(pady=10)

    frame_rolagem = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
    frame_rolagem.pack(fill="both", expand=True)

    cursor_lista = root.conn.cursor(dictionary=True)
    consulta_listar = "SELECT * FROM produtos"
    cursor_lista.execute(consulta_listar)

    for produto in cursor_lista.fetchall():
        card_produto = ctk.CTkFrame(frame_rolagem, fg_color="white", corner_radius=10)
        card_produto.pack(fill="x", pady=5, padx=10)

        ctk.CTkLabel(card_produto, text=f"{produto['nome_produto']}", font=("Arial", 13, "bold")).pack(side="left", padx=15)
        ctk.CTkLabel(card_produto, text=f"R$ {produto['preco']:.2f}", font=("Arial", 12)).pack(side="left", padx=20)

        ctk.CTkButton(card_produto, text="Excluir", fg_color=COR_EXCLUIR, width=60, 
                      command=lambda id_p=produto['id_produto']: excluir_item(id_p, "produtos")).pack(side="right", padx=10)
        
        ctk.CTkButton(card_produto, text="Editar", fg_color=COR_EDITAR, width=60, 
                      command=lambda d_p=produto: abrir_formulario_produto(d_p)).pack(side="right", padx=5)

    cursor_lista.close()
  

# =======================
# TELA DE PEDIDOS
# =======================

def tela_pedidos():
    limpar_main()
    ctk.CTkLabel(main_frame, text="Pedidos 📋", font=("Arial", 24, "bold")).pack(pady=20)

    def abrir_formulario_pedido(dados_pedido=None):
        janela_formulario = ctk.CTkToplevel(root)
        janela_formulario.geometry("450x600")
        janela_formulario.attributes("-topmost", True)
        janela_formulario.title("Editar Pedido" if dados_pedido else "Novo Pedido")
        
        cursor_setup = root.conn.cursor()
        cursor_setup.execute("SELECT id_cliente, nome FROM cliente")
        dicionario_clientes = {nome: id_cli for id_cli, nome in cursor_setup.fetchall()}
        
        cursor_setup.execute("SELECT id_produto, nome_produto, preco FROM produtos")
        dicionario_produtos = {nome: (id_prod, preco) for id_prod, nome, preco in cursor_setup.fetchall()}
        cursor_setup.close()

        ctk.CTkLabel(janela_formulario, text="Nome do Cliente:").pack(pady=(10, 0))
        combo_cliente = ctk.CTkComboBox(janela_formulario, values=list(dicionario_clientes.keys()), width=300)
        combo_cliente.pack(pady=5)

        ctk.CTkLabel(janela_formulario, text="Item (Produto):").pack(pady=(10, 0))
        combo_produto = ctk.CTkComboBox(janela_formulario, values=list(dicionario_produtos.keys()), width=300)
        combo_produto.pack(pady=5)

        ctk.CTkLabel(janela_formulario, text="Quantidade:").pack(pady=(10, 0))
        entrada_quantidade = ctk.CTkEntry(janela_formulario, width=300)
        entrada_quantidade.insert(0, "1")
        entrada_quantidade.pack(pady=5)

        ctk.CTkLabel(janela_formulario, text="Status do Pedido:").pack(pady=(10, 0))
        combo_status = ctk.CTkComboBox(janela_formulario, values=['Em preparo', 'Saiu para entrega', 'Entregue'], width=300)
        combo_status.pack(pady=5)

        if dados_pedido:
            combo_cliente.set(dados_pedido['nome_cliente'])
            combo_produto.set(dados_pedido['nome_produto'])
            entrada_quantidade.delete(0, 'end')
            entrada_quantidade.insert(0, str(dados_pedido['quantidade']))
            combo_status.set(dados_pedido['status_pedido'])
        
        def salvar_pedido():
            try:
                id_cliente = dicionario_clientes[combo_cliente.get()]
                id_produto, preco_unitario = dicionario_produtos[combo_produto.get()]
                quantidade = int(entrada_quantidade.get())
                status = combo_status.get()
                valor_total = float(preco_unitario) * quantidade
                
                cursor_db = root.conn.cursor()
                if dados_pedido:
                    consulta_pedido = "UPDATE pedidos SET id_cliente=%s, valor_total=%s, status_pedido=%s WHERE id_pedidos=%s"
                    cursor_db.execute(consulta_pedido, (id_cliente, valor_total, status, dados_pedido['id_pedidos']))
                    
                    consulta_item = "UPDATE itens_pedidos SET id_produto=%s, quantidade=%s WHERE id_pedido=%s"
                    cursor_db.execute(consulta_item, (id_produto, quantidade, dados_pedido['id_pedidos']))
                else:
                    consulta_pedido = "INSERT INTO pedidos (id_cliente, valor_total, status_pedido, data_hora) VALUES (%s,%s,%s,NOW())"
                    cursor_db.execute(consulta_pedido, (id_cliente, valor_total, status))
                    
                    id_novo_pedido = cursor_db.lastrowid
                    consulta_item = "INSERT INTO itens_pedidos (id_pedido, id_produto, quantidade) VALUES (%s,%s,%s)"
                    cursor_db.execute(consulta_item, (id_novo_pedido, id_produto, quantidade))
                
                root.conn.commit()
                cursor_db.close()
                janela_formulario.destroy()
                tela_pedidos()
            except: 
                messagebox.showerror("Erro", "Verifique as opções!")
        
        ctk.CTkButton(janela_formulario, text="Salvar", fg_color=COR_BOTAO, command=salvar_pedido).pack(pady=20)

    ctk.CTkButton(main_frame, text="+ Novo Pedido", fg_color=COR_BOTAO, command=lambda: abrir_formulario_pedido()).pack(pady=10)
    
    frame_rolagem = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
    frame_rolagem.pack(fill="both", expand=True)
    
    cursor_lista = root.conn.cursor(dictionary=True)
    consulta_busca = """
        SELECT p.*, c.nome as nome_cliente, pr.nome_produto, i.quantidade, DATE_FORMAT(p.data_hora, '%%d/%%m %%H:%%i') as data_formatada 
        FROM pedidos p JOIN cliente c ON p.id_cliente = c.id_cliente 
        JOIN itens_pedidos i ON p.id_pedidos = i.id_pedido JOIN produtos pr ON i.id_produto = pr.id_produto 
        ORDER BY p.id_pedidos DESC"""
    cursor_lista.execute(consulta_busca)
    
    for pedido in cursor_lista.fetchall():
        card_pedido = ctk.CTkFrame(frame_rolagem, fg_color="white", corner_radius=10)
        card_pedido.pack(fill="x", pady=5, padx=10)
        
        texto_info = f"ID: #{pedido['id_pedidos']} | Cliente: {pedido['nome_cliente']}\n{pedido['nome_produto']} (Qtd: {pedido['quantidade']})"
        
        ctk.CTkLabel(card_pedido, text=texto_info, font=("Arial", 12, "bold"), justify="left").pack(side="left", padx=20, pady=10)
        ctk.CTkLabel(card_pedido, text=f"Data: {pedido['data_formatada']}", font=("Arial", 11), text_color="gray").pack(side="left", padx=30)
        
        ctk.CTkButton(card_pedido, text="Excluir", fg_color=COR_EXCLUIR, width=60, 
                      command=lambda id_p=pedido['id_pedidos']: excluir_item(id_p, "pedidos")).pack(side="right", padx=10)
        
        ctk.CTkButton(card_pedido, text="Editar", fg_color=COR_EDITAR, width=60, 
                      command=lambda d_p=pedido: abrir_formulario_pedido(d_p)).pack(side="right", padx=5)
        
        ctk.CTkLabel(card_pedido, text=f"{pedido['status_pedido']} | R$ {pedido['valor_total']:.2f}", 
                     font=("Arial", 12, "bold"), text_color="#2E7D32").pack(side="right", padx=15)
    
    cursor_lista.close()


def excluir_item(id_item, tabela):
    if messagebox.askyesno("Confirmar", f"Excluir item?"):
        try:
            cursor_excluir = root.conn.cursor()
            mapeamento_tabelas = {"produtos": "id_produto", "cliente": "id_cliente", "pedidos": "id_pedidos"}
            
            consulta_excluir = f"DELETE FROM {tabela} WHERE {mapeamento_tabelas[tabela]} = %s"
            cursor_excluir.execute(consulta_excluir, (id_item,))
            
            root.conn.commit()
            cursor_excluir.close()
            # Atualiza a tela chamando a função global dinamicamente
            globals()[f"tela_{tabela}"]()
        except: 
            messagebox.showerror("Erro", "Remova vínculos no banco primeiro.")


# =======================
# LOGIN E INICIALIZAÇÃO
# =======================
def fazer_login():
    email = email_entry.get().strip()
    senha = password_entry.get().strip()
    try:
        conexao = connect_to_database()
        cursor_login = conexao.cursor()
        
        consulta_verificar = "SELECT senha FROM login WHERE email=%s"
        cursor_login.execute(consulta_verificar, (email,))
        resultado = cursor_login.fetchone()
        
        if resultado and resultado[0] == senha:
            login_win.destroy()
            iniciar_sistema()
        else:
            messagebox.showerror("Erro", "E-mail ou senha inválidos.")
            
        cursor_login.close()
        conexao.close()
    except Exception as erro:
        messagebox.showerror("Erro", f"Erro de conexão: {erro}")

def abrir_cadastro():
    login_win.withdraw()
    janela_cadastro = ctk.CTkToplevel(login_win)
    janela_cadastro.geometry("400x500")
    janela_cadastro.title("Criar Conta")
    
    entrada_email_cad = ctk.CTkEntry(janela_cadastro, placeholder_text="Email", width=300)
    entrada_email_cad.pack(pady=20)
    
    entrada_senha_cad = ctk.CTkEntry(janela_cadastro, placeholder_text="Senha", show="*", width=300)
    entrada_senha_cad.pack(pady=10)
    
    def salvar_novo_usuario():
        try:
            conexao = connect_to_database()
            cursor_cad = conexao.cursor()
            
            consulta_cadastrar = "INSERT INTO login (email, senha) VALUES (%s, %s)"
            cursor_cad.execute(consulta_cadastrar, (entrada_email_cad.get(), entrada_senha_cad.get()))
            
            conexao.commit()
            cursor_cad.close()
            conexao.close()
            janela_cadastro.destroy()
            login_win.deiconify()
        except:
            messagebox.showerror("Erro", "E-mail já existe!")
            
    ctk.CTkButton(janela_cadastro, text="Cadastrar", fg_color=ORANGE, command=salvar_novo_usuario).pack(pady=20)
    
    # Se fechar a janela no 'X', volta para a tela de login
    janela_cadastro.protocol("WM_DELETE_WINDOW", lambda: (janela_cadastro.destroy(), login_win.deiconify()))

# --- Interface de Login ---
login_win = ctk.CTk()
login_win.title("Login - Pizzaloop")
login_win.geometry("1200x600")

# Painel Lateral (Logo)
frame_lateral = ctk.CTkFrame(login_win, width=350, fg_color=DARK, corner_radius=0)
frame_lateral.pack(side="left", fill="y")

ctk.CTkLabel(frame_lateral, text="🍕 Pizzaloop", font=("Arial", 24, "bold"), text_color="white").place(relx=0.5, rely=0.4, anchor="center")

# Painel Direito (Formulário)
frame_principal = ctk.CTkFrame(login_win, fg_color=LIGHT_BG, corner_radius=0)
frame_principal.pack(side="right", fill="both", expand=True)

# Card de Login centralizado
card_login = ctk.CTkFrame(frame_principal, width=350, height=400, corner_radius=15, fg_color="white")
card_login.place(relx=0.5, rely=0.5, anchor="center")

email_entry = ctk.CTkEntry(card_login, placeholder_text="Email", width=260)
email_entry.pack(pady=(50, 10))

password_entry = ctk.CTkEntry(card_login, placeholder_text="Senha", show="*", width=260)
password_entry.pack(pady=10)

ctk.CTkButton(card_login, text="Entrar", fg_color=ORANGE, command=fazer_login).pack(pady=20)

link_cadastro = ctk.CTkLabel(card_login, text="Criar conta", cursor="hand2", text_color="gray")
link_cadastro.pack()
link_cadastro.bind("<Button-1>", lambda e: abrir_cadastro())

login_win.mainloop()    
'''