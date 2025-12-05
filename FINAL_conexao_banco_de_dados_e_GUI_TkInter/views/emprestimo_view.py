import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import date 

class TelaEmprestimo(tk.Frame):
    """
    Frame contêiner para realizar o CRUD da entidade Empréstimo.
    """
    def __init__(self, master=None, controlador=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.atributos = [
            "id", "id_cliente", "id_livro", "data_emprestimo", "data_prevista_devolucao", "data_efetiva_devolucao"
        ]
        self.controlador = controlador
        
        self.widgets = {}
        self._criar_formulario()
        self._criar_botoes()
        self._criar_tabela()
        
        self.carregar_dados_iniciais()

    def _criar_formulario(self):
        form_frame = ttk.LabelFrame(self, text="📝 Dados do Empréstimo")
        form_frame.pack(fill="x", padx=5, pady=5)
        
        row = 0
        
        for atributo in self.atributos:
            # data_emprestimo e data_prevista_devolucao são definidas pelo modelo, não editadas aqui.
            # A única coisa que editamos é a data_efetiva_devolucao.
            if atributo in ["data_emprestimo", "data_prevista_devolucao"]:
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
        
        # O botão Salvar aqui inicia um novo empréstimo
        ttk.Button(button_frame, text="✅ Iniciar Empréstimo", command=self.event_bt_salvar).pack(side="left", padx=5, pady=5)
        
        # O botão Atualizar aqui geralmente define a data_efetiva_devolucao (Devolução)
        ttk.Button(button_frame, text="⏎ Devolver Livro", command=self.event_bt_atualizar_registro).pack(side="left", padx=5, pady=5)
        
        # Deletar (raramente usado em empréstimos)
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
        self.tree.column("id_cliente", width=80)
        self.tree.column("id_livro", width=80)
        self.tree.column("data_emprestimo", width=120)
        self.tree.column("data_prevista_devolucao", width=120)
        self.tree.column("data_efetiva_devolucao", width=120)
        
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
        
        # Adiciona dados que não estão no form (usados pelo modelo para inserir/atualizar)
        for attr in ["data_emprestimo", "data_prevista_devolucao"]:
             if attr not in dados: dados[attr] = None
        
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
    
    def atualizar_tabela(self, lista_emprestimos):
        self.tree.delete(*self.tree.get_children())
        colunas = self.atributos
        
        if lista_emprestimos:
            for emp_dict in lista_emprestimos:
                valores_formatados = [emp_dict.get(attr, '') for attr in colunas]
                self.tree.insert('', tk.END, values=valores_formatados)
                
    def carregar_dados_iniciais(self):
        # ATENÇÃO: Referência ao gerenciador gEmprestimo
        if self.controlador and hasattr(self.controlador, 'gEmprestimo'):
            try:
                lista_emprestimos = self.controlador.gEmprestimo.listar() 
                self.atualizar_tabela(lista_emprestimos)
            except Exception as e:
                messagebox.showerror("Erro de BD", f"Não foi possível carregar os empréstimos: {e}")
        else:
            self.atualizar_tabela([])
            
    # --- EVENTOS DE CRUD ---

    def event_bt_salvar(self):
        """Inicia um novo empréstimo (Salvar)."""
        dados = self.capturar_dados()

        if dados['id'] != 0:
            messagebox.showwarning("Aviso", "Limpe os campos para iniciar um novo empréstimo.")
            return

        id_cliente = dados['id_cliente']
        id_livro = dados['id_livro']
        
        if not id_cliente or not id_livro:
            messagebox.showwarning("Aviso", "Preencha ID do Cliente e ID do Livro.")
            return
        
        try:
            # ATENÇÃO: Método salvar do gEmprestimo
            self.controlador.gEmprestimo.salvar(id_cliente, id_livro)
            self.limpar_campos()
            self.carregar_dados_iniciais()
            messagebox.showinfo("Sucesso", "Empréstimo iniciado com sucesso!")
        except Exception as e:
             messagebox.showerror("Erro ao Iniciar", f"Não foi possível iniciar o empréstimo: {e}")

    def event_bt_atualizar_registro(self):
        """Finaliza um empréstimo (Devolução)."""
        dados = self.capturar_dados()
        
        if dados['id'] == 0:
            messagebox.showwarning("Aviso", "Selecione um empréstimo na tabela para registrar a devolução.")
            return
            
        id_emprestimo = dados['id']
        # data_efetiva_devolucao pode ser pega do formulário ou definida automaticamente.
        data_efetiva = dados['data_efetiva_devolucao'] if dados.get('data_efetiva_devolucao') else date.today().strftime('%Y-%m-%d')
        
        try:
            # ATENÇÃO: Método atualizar (devolver) do gEmprestimo
            self.controlador.gEmprestimo.atualizar(id_emprestimo, data_efetiva)
            self.limpar_campos()
            self.carregar_dados_iniciais()
            messagebox.showinfo("Sucesso", f"Devolução registrada para Empréstimo ID {id_emprestimo}!")
        except Exception as e:
             messagebox.showerror("Erro na Devolução", f"Não foi possível registrar a devolução: {e}")
             
    def event_bt_deletar(self):
        id_valor = self.capturar_dados()['id']
        
        if id_valor == 0:
            messagebox.showwarning("Aviso", "Selecione um empréstimo na tabela para deletar.")
            return
            
        confirmar = messagebox.askyesno(
            "Confirmação", 
            f"Tem certeza que deseja DELETAR o Empréstimo ID {id_valor}?"
        )
        
        if confirmar:
            try:
                # ATENÇÃO: Método deletar do gEmprestimo
                self.controlador.gEmprestimo.deletar(id_valor)
                self.limpar_campos()
                self.carregar_dados_iniciais()
                messagebox.showinfo("Sucesso", f"Empréstimo ID {id_valor} deletado com sucesso!")
            except Exception as e:
                 messagebox.showerror("Erro ao Deletar", f"Não foi possível deletar o empréstimo: {e}")