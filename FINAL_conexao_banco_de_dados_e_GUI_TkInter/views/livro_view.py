import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import date # Usado para consistência, mas não diretamente necessário para Livro

class TelaLivro(tk.Frame):
    """
    Frame contêiner para realizar o CRUD da entidade Livro.
    """
    def __init__(self, master=None, controlador=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.atributos = [
            "id", "id_autor", "titulo_livro", "ISBN", "ano_publicacao", "is_emprestado"
        ]
        self.controlador = controlador
        
        self.widgets = {}
        self._criar_formulario()
        self._criar_botoes()
        self._criar_tabela()
        
        self.carregar_dados_iniciais()

    def _criar_formulario(self):
        form_frame = ttk.LabelFrame(self, text="📚 Dados do Livro")
        form_frame.pack(fill="x", padx=5, pady=5)
        
        row = 0
        
        for atributo in self.atributos:
            # is_emprestado e ID são apenas exibidos/manuseados internamente
            if atributo == "is_emprestado":
                continue 
                
            label_text = f"{atributo.replace('_', ' ').capitalize()}:"
            label = ttk.Label(form_frame, text=label_text)
            label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
            
            var = tk.StringVar()
            entry = ttk.Entry(form_frame, textvariable=var, width=40)
            entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
            
            if atributo == 'id':
                entry.config(state='readonly', foreground='gray')
            
            self.widgets[atributo] = entry 
            row += 1
                 
        form_frame.grid_columnconfigure(1, weight=1)

    def _criar_botoes(self):
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(button_frame, text="✅ Salvar", command=self.event_bt_salvar).pack(side="left", padx=5, pady=5)
        ttk.Button(button_frame, text="🔄 Atualizar", command=self.event_bt_atualizar_registro).pack(side="left", padx=5, pady=5)
        ttk.Button(button_frame, text="🗑️ Deletar", command=self.event_bt_deletar).pack(side="left", padx=5, pady=5)
        ttk.Button(button_frame, text="🧹 Limpar Campos", command=self.limpar_campos).pack(side="right", padx=5, pady=5)

    def _criar_tabela(self):
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=5, pady=5)

        colunas = self.atributos
        self.tree = ttk.Treeview(table_frame, columns=colunas, show='headings')
        
        for col in colunas:
            self.tree.heading(col, text=col.replace('_', ' ').upper())
            self.tree.column(col, width=100, anchor=tk.CENTER)
            
        self.tree.column("id", width=50)
        self.tree.column("titulo_livro", width=200, anchor=tk.W)
        self.tree.column("id_autor", width=80)
        self.tree.column("is_emprestado", width=100)
        
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<Double-1>", self.carregar_campos_selecao) 
        self.tree.bind("<<TreeviewSelect>>", self._on_treeview_select)

    def capturar_dados(self):
        dados = {}
        for atributo in self.atributos:
            if atributo in self.widgets:
                widget = self.widgets[atributo]
                valor = widget.get().strip()
                
                if atributo == 'id':
                    try:
                        valor = int(valor) if valor else 0
                    except ValueError:
                        valor = 0
                        
                dados[atributo] = valor
        
        # O campo is_emprestado não está no form, mas é necessário para o modelo
        dados['is_emprestado'] = 0 # Assume 0 (False) para novo ou 0/1 para atualização (pode ser ajustado)
        return dados
    
    def limpar_campos(self):
        for atributo in self.atributos:
             if atributo in self.widgets:
                widget = self.widgets[atributo]
                if atributo == 'id':
                    widget.config(state='normal')
                    widget.delete(0, tk.END)
                    widget.config(state='readonly')
                else:
                    widget.delete(0, tk.END)

    def _on_treeview_select(self, event):
        pass
        
    def carregar_campos_selecao(self, event):
        selecao = self.tree.focus()
        if selecao:
            valores = self.tree.item(selecao, 'values')
            
            for i, atributo in enumerate(self.atributos):
                valor = valores[i]
                
                if atributo in self.widgets:
                    entry = self.widgets[atributo]
                    
                    if atributo == 'id':
                        entry.config(state='normal')
                        entry.delete(0, tk.END)
                        entry.insert(0, valor)
                        entry.config(state='readonly')
                    else:
                        entry.delete(0, tk.END)
                        entry.insert(0, valor)
    
    def atualizar_tabela(self, lista_livros):
        self.tree.delete(*self.tree.get_children())
        colunas = self.atributos
        
        if lista_livros:
            for livro_dict in lista_livros:
                valores_formatados = [livro_dict.get(attr, '') for attr in colunas]
                self.tree.insert('', tk.END, values=valores_formatados)
                
    def carregar_dados_iniciais(self):
        # ATENÇÃO: Referência ao gerenciador gLivro
        if self.controlador and hasattr(self.controlador, 'gLivro'):
            try:
                lista_livros = self.controlador.gLivro.listar() 
                self.atualizar_tabela(lista_livros)
            except Exception as e:
                messagebox.showerror("Erro de BD", f"Não foi possível carregar os livros: {e}")
        else:
            self.atualizar_tabela([])
            
    # --- EVENTOS DE CRUD ---

    def event_bt_salvar(self):
        dados = self.capturar_dados()

        if dados['id'] != 0:
            messagebox.showwarning("Aviso", "Limpe os campos para salvar um novo livro.")
            return

        id_autor = dados['id_autor']
        titulo_livro = dados['titulo_livro']
        ISBN = dados['ISBN']
        ano_publicacao = dados['ano_publicacao']
        
        try:
            # ATENÇÃO: Método salvar do gLivro
            self.controlador.gLivro.salvar(id_autor, titulo_livro, ISBN, ano_publicacao)
            self.limpar_campos()
            self.carregar_dados_iniciais()
            messagebox.showinfo("Sucesso", "Livro salvo com sucesso!")
        except Exception as e:
             messagebox.showerror("Erro ao Salvar", f"Não foi possível salvar o livro: {e}")

    def event_bt_atualizar_registro(self):
        dados = self.capturar_dados()
        
        if dados['id'] == 0:
            messagebox.showwarning("Aviso", "Selecione um livro na tabela para atualizar.")
            return
            
        id_livro = dados['id']
        id_autor = dados['id_autor']
        titulo_livro = dados['titulo_livro']
        ISBN = dados['ISBN']
        ano_publicacao = dados['ano_publicacao']
        is_emprestado = dados['is_emprestado'] # Pode ser 0 ou 1
        
        try:
            # ATENÇÃO: Método atualizar do gLivro
            self.controlador.gLivro.atualizar(id_livro, id_autor, titulo_livro, ISBN, ano_publicacao, is_emprestado)
            self.limpar_campos()
            self.carregar_dados_iniciais()
            messagebox.showinfo("Sucesso", f"Livro ID {id_livro} atualizado com sucesso!")
        except Exception as e:
             messagebox.showerror("Erro ao Atualizar", f"Não foi possível atualizar o livro: {e}")
             
    def event_bt_deletar(self):
        id_valor = self.capturar_dados()['id']
        
        if id_valor == 0:
            messagebox.showwarning("Aviso", "Selecione um livro na tabela para deletar.")
            return
            
        confirmar = messagebox.askyesno(
            "Confirmação", 
            f"Tem certeza que deseja DELETAR o Livro ID {id_valor}?"
        )
        
        if confirmar:
            try:
                # ATENÇÃO: Método deletar do gLivro
                self.controlador.gLivro.deletar(id_valor)
                self.limpar_campos()
                self.carregar_dados_iniciais()
                messagebox.showinfo("Sucesso", f"Livro ID {id_valor} deletado com sucesso!")
            except Exception as e:
                 messagebox.showerror("Erro ao Deletar", f"Não foi possível deletar o livro: {e}")