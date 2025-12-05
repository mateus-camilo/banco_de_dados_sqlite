import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import date # Importar se necessário para validação/formato

class TelaCliente(tk.Frame):
    """
    Frame contêiner para realizar o CRUD da entidade Cliente.
    """
    def __init__(self, master=None, controlador=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.atributos = [
            "id", "nome", "email", "data_nascimento", "total_emprestimo"
        ]
        self.controlador = controlador
        
        self.widgets = {}
        self._criar_formulario()
        self._criar_botoes()
        self._criar_tabela()
        
        self.carregar_dados_iniciais()

    def _criar_formulario(self):
        form_frame = ttk.LabelFrame(self, text="👤 Dados do Cliente")
        form_frame.pack(fill="x", padx=5, pady=5)
        
        row = 0
        
        for atributo in self.atributos:
            # O campo total_emprestimo será apenas exibido e não editável
            if atributo == "total_emprestimo":
                continue # Pula a criação de um campo editável
                
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
        self.tree.column("nome", width=150, anchor=tk.W)
        self.tree.column("email", width=180, anchor=tk.W)
        self.tree.column("total_emprestimo", width=100)
        
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
            elif atributo == 'total_emprestimo':
                # Campo não existe no form de entrada, então ignoramos
                continue
            
            if atributo == 'id':
                try:
                    valor = int(valor) if valor else 0
                except ValueError:
                    valor = 0
            
            dados[atributo] = valor
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
    
    def atualizar_tabela(self, lista_clientes):
        self.tree.delete(*self.tree.get_children())
        colunas = self.atributos
        
        if lista_clientes:
            for cliente_dict in lista_clientes:
                valores_formatados = [cliente_dict.get(attr, '') for attr in colunas]
                self.tree.insert('', tk.END, values=valores_formatados)
                
    def carregar_dados_iniciais(self):
        # ATENÇÃO: Referência ao gerenciador gCliente
        if self.controlador and hasattr(self.controlador, 'gCliente'):
            try:
                lista_clientes = self.controlador.gCliente.listar() 
                self.atualizar_tabela(lista_clientes)
            except Exception as e:
                messagebox.showerror("Erro de BD", f"Não foi possível carregar os clientes: {e}")
        else:
            self.atualizar_tabela([])
            
    # --- EVENTOS DE CRUD ---

    def event_bt_salvar(self):
        dados = self.capturar_dados()

        if dados['id'] != 0:
            messagebox.showwarning("Aviso", "Limpe os campos para salvar um novo cliente.")
            return

        nome = dados['nome']
        email = dados['email']
        data_nascimento = dados['data_nascimento']
        
        try:
            # ATENÇÃO: Método salvar do gCliente
            self.controlador.gCliente.salvar(email, nome, data_nascimento)
            self.limpar_campos()
            self.carregar_dados_iniciais()
            messagebox.showinfo("Sucesso", "Cliente salvo com sucesso!")
        except Exception as e:
             messagebox.showerror("Erro ao Salvar", f"Não foi possível salvar o cliente: {e}")

    def event_bt_atualizar_registro(self):
        dados = self.capturar_dados()
        
        if dados['id'] == 0:
            messagebox.showwarning("Aviso", "Selecione um cliente na tabela para atualizar.")
            return
            
        id_cliente = dados['id']
        nome = dados['nome']
        email = dados['email']
        data_nascimento = dados['data_nascimento']
        
        try:
            # ATENÇÃO: Método atualizar do gCliente
            self.controlador.gCliente.atualizar(email, nome, data_nascimento, id_cliente)
            self.limpar_campos()
            self.carregar_dados_iniciais()
            messagebox.showinfo("Sucesso", f"Cliente ID {id_cliente} atualizado com sucesso!")
        except Exception as e:
             messagebox.showerror("Erro ao Atualizar", f"Não foi possível atualizar o cliente: {e}")
             
    def event_bt_deletar(self):
        id_valor = self.capturar_dados()['id']
        
        if id_valor == 0:
            messagebox.showwarning("Aviso", "Selecione um cliente na tabela para deletar.")
            return
            
        confirmar = messagebox.askyesno(
            "Confirmação", 
            f"Tem certeza que deseja DELETAR o Cliente ID {id_valor}?"
        )
        
        if confirmar:
            try:
                # ATENÇÃO: Método deletar do gCliente
                self.controlador.gCliente.deletar(id_valor)
                self.limpar_campos()
                self.carregar_dados_iniciais()
                messagebox.showinfo("Sucesso", f"Cliente ID {id_valor} deletado com sucesso!")
            except Exception as e:
                 messagebox.showerror("Erro ao Deletar", f"Não foi possível deletar o cliente: {e}")