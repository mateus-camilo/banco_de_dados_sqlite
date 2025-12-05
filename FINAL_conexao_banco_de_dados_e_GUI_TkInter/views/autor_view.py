import tkinter as tk
from tkinter import ttk
from datetime import date
from tkinter import messagebox # Importar para exibir mensagens de erro/sucesso

class TelaAutor(tk.Frame):
    """
    Frame contêiner para realizar o CRUD da entidade Autor.
    """
    # CORREÇÃO 1: Capturar 'controlador' separadamente do 'master' e usar **kwargs
    def __init__(self, master=None, controlador=None, **kwargs):
        # Passa apenas o master e as opções Tkinter para o super()
        super().__init__(master, **kwargs)
        
        self.atributos = [
            "id", "nome", "data_nascimento", "biografia"
        ]
        self.controlador = controlador
        
        self.widgets = {} # Dicionário para armazenar as Entrys
        self._criar_formulario()
        self._criar_botoes()
        self._criar_tabela()
        
        # Opcional: Chama para carregar os dados iniciais na tabela ao abrir a tela
        self.carregar_dados_iniciais()

    def _criar_formulario(self):
        form_frame = ttk.LabelFrame(self, text="👤 Dados do Autor")
        form_frame.pack(fill="x", padx=5, pady=5)
        
        # Grid para o formulário
        row = 0
        
        for indice, atributo in enumerate(self.atributos):
            # O campo Biografia será colocado em uma linha separada
            if atributo == "biografia":
                row += 1
                
            # --- LABEL ---
            label_text = f"{atributo.replace('_', ' ').capitalize()}:"
            label = ttk.Label(form_frame, text=label_text)
            label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
            
            # --- CAMPO DE ENTRADA ---
            
            # 1. Biografia (Text Area maior)
            if atributo == 'biografia':
                entry = tk.Text(form_frame, height=4, width=70)
                entry.grid(row=row, column=1, columnspan=3, padx=5, pady=5, sticky="ew")
            
            # 2. Outros campos (Entry padrão)
            else:
                var = tk.StringVar()
                entry = ttk.Entry(form_frame, textvariable=var, width=30)
                entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
                
                # Campo ID (Não editável)
                if atributo == 'id':
                    entry.config(state='readonly', foreground='gray')
            
            # CORREÇÃO 2: Mover o mapeamento para fora do if/else para incluir todos os widgets
            self.widgets[atributo] = entry 
            
            # Avança a linha apenas para os campos que não são biografia
            if atributo != "biografia":
                 row += 1
                 
        # Garante que o campo de entrada do formulário se expanda horizontalmente
        form_frame.grid_columnconfigure(1, weight=1)

    def _criar_botoes(self):
        """Cria os botões de CRUD e Limpar, ligando os comandos."""
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        # Botões
        ttk.Button(button_frame, text="✅ Salvar", command=self.event_bt_salvar).pack(side="left", padx=5, pady=5)
        
        # LIGAÇÃO DO NOVO EVENTO DE ATUALIZAR
        ttk.Button(button_frame, text="🔄 Atualizar", command=self.event_bt_atualizar_registro).pack(side="left", padx=5, pady=5)
        
        # LIGAÇÃO DO NOVO EVENTO DE DELETAR
        ttk.Button(button_frame, text="🗑️ Deletar", command=self.event_bt_deletar).pack(side="left", padx=5, pady=5)
        
        ttk.Button(button_frame, text="🧹 Limpar Campos", command=self.limpar_campos).pack(side="right", padx=5, pady=5)

    def _criar_tabela(self):
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Configuração das colunas do Treeview
        colunas = self.atributos
        self.tree = ttk.Treeview(table_frame, columns=colunas, show='headings')
        
        # Define os títulos das colunas
        for col in colunas:
            self.tree.heading(col, text=col.replace('_', ' ').upper())
            self.tree.column(col, width=100, anchor=tk.CENTER)
            
        # Ajustes de Largura específicos
        self.tree.column("id", width=50)
        self.tree.column("nome", width=150, anchor=tk.W)
        self.tree.column("data_nascimento", width=100)
        self.tree.column("biografia", width=300, anchor=tk.W)
        
        # Adicionar Barra de Rolagem
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        
        # Layout
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Associa o duplo clique para carregar campos
        self.tree.bind("<Double-1>", self.carregar_campos_selecao) 
        
        # Associa a seleção única (<<TreeviewSelect>>) para um método auxiliar
        self.tree.bind("<<TreeviewSelect>>", self._on_treeview_select)


    # --- Métodos de Captura e Limpeza de Dados ---

    def capturar_dados(self):
        """Retorna um dicionário contendo os valores atuais de todos os campos do formulário."""
        dados = {}
        for atributo, widget in self.widgets.items():
            if isinstance(widget, tk.Text):
                valor = widget.get('1.0', tk.END).strip()
            else:
                valor = widget.get().strip()
            
            if atributo == 'id':
                try:
                    valor = int(valor) if valor else 0
                except ValueError:
                    valor = 0 # Trata IDs inválidos
            
            dados[atributo] = valor
        return dados

    def limpar_campos(self):
        """Limpa todos os campos do formulário."""
        for atributo, widget in self.widgets.items():
            if isinstance(widget, tk.Text):
                 widget.delete('1.0', tk.END)
            else:
                if atributo == 'id':
                    widget.config(state='normal')
                    widget.delete(0, tk.END)
                    widget.config(state='readonly')
                else:
                    widget.delete(0, tk.END)

    def _on_treeview_select(self, event):
        """Método auxiliar para evitar que a seleção dispare o carregamento de campos (se você usar Double-1)."""
        pass
        
    def carregar_campos_selecao(self, event):
        """Carrega os dados da linha selecionada para os campos de entrada."""
        selecao = self.tree.focus()
        if selecao:
            valores = self.tree.item(selecao, 'values')
            
            for i, atributo in enumerate(self.atributos):
                valor = valores[i]
                
                # Lógica específica para Text Widget (biografia)
                if atributo == 'biografia':
                    # O self.widgets[atributo] é o Text widget
                    self.widgets[atributo].delete('1.0', tk.END) 
                    self.widgets[atributo].insert('1.0', valor)
                    continue

                # Lógica para Entrys (id, nome, data_nascimento)
                entry = self.widgets[atributo]
                
                # Se for o ID, precisa mudar o estado temporariamente
                if atributo == 'id':
                    entry.config(state='normal')
                    entry.delete(0, tk.END)
                    entry.insert(0, valor)
                    entry.config(state='readonly')
                else:
                    entry.delete(0, tk.END)
                    entry.insert(0, valor)
    
    def atualizar_tabela(self, lista_autores):
        """Limpa a Treeview e a repopula com os dados fornecidos na lista_autores."""
        # 1. Limpar todos os itens existentes na tabela
        self.tree.delete(*self.tree.get_children())
        
        colunas = self.atributos # ['id', 'nome', 'data_nascimento', 'biografia']
        
        # 2. Popular a tabela com a nova lista de autores
        if lista_autores:
            for autor_dict in lista_autores:
                
                # Coleta os valores do dicionário na ordem correta das colunas (self.atributos)
                # O método .get() é usado para evitar KeyErrors, retornando '' se a chave faltar.
                valores_formatados = [autor_dict.get(attr, '') for attr in colunas]
                
                # Insere a tupla de valores formatados na Treeview
                self.tree.insert('', tk.END, values=valores_formatados)
                
    def carregar_dados_iniciais(self):
        """Busca os dados no modelo e atualiza a tabela."""
        if self.controlador and hasattr(self.controlador, 'gAutor'):
            try:
                lista_autores = self.controlador.gAutor.listar() 
                self.atualizar_tabela(lista_autores)
            except Exception as e:
                messagebox.showerror("Erro de BD", f"Não foi possível carregar os autores: {e}")
        else:
            self.atualizar_tabela([])
            
    # --- EVENTOS DE CRUD ---

    def event_bt_salvar(self):
        dados = self.capturar_dados()

        # O ID deve ser 0 para SALVAR (nova inserção)
        if dados['id'] != 0:
            messagebox.showwarning("Aviso", "Limpe os campos para salvar um novo autor.")
            return

        nome = dados['nome']
        data_nascimento = dados['data_nascimento']
        biografia = dados['biografia']
        
        try:
            self.controlador.gAutor.salvar(nome, data_nascimento, biografia)
            self.limpar_campos()
            self.carregar_dados_iniciais() # Atualiza a tabela
            messagebox.showinfo("Sucesso", "Autor salvo com sucesso!")
        except Exception as e:
             messagebox.showerror("Erro ao Salvar", f"Não foi possível salvar o autor: {e}")

    # MÉTODO: ATUALIZAR REGISTRO (chamado pelo botão)
    def event_bt_atualizar_registro(self):
        """Pega os dados do formulário e envia para o modelo atualizar."""
        dados = self.capturar_dados()
        
        # 1. VALIDAÇÃO: Verifica se o ID é válido (necessário para atualização)
        if dados['id'] == 0:
            messagebox.showwarning("Aviso", "Selecione um autor na tabela para atualizar.")
            return
            
        id_autor = dados['id']
        nome = dados['nome']
        data_nascimento = dados['data_nascimento']
        biografia = dados['biografia']
        
        try:
            self.controlador.gAutor.atualizar(id_autor, nome, data_nascimento, biografia)
            self.limpar_campos()
            self.carregar_dados_iniciais() # Atualiza a tabela
            messagebox.showinfo("Sucesso", f"Autor ID {id_autor} atualizado com sucesso!")
        except Exception as e:
             messagebox.showerror("Erro ao Atualizar", f"Não foi possível atualizar o autor: {e}")
             
    # MÉTODO: DELETAR REGISTRO
    def event_bt_deletar(self):
        """Deleta o registro selecionado, validando se o campo ID está preenchido."""
        
        # Pega o valor do ID (e converte para int, se possível)
        id_valor = self.capturar_dados()['id']
        
        # 1. VALIDAÇÃO: Verifica se o campo ID está preenchido
        if id_valor == 0:
            messagebox.showwarning("Aviso", "Selecione um autor na tabela para deletar.")
            return
            
        # 2. Confirmação
        confirmar = messagebox.askyesno(
            "Confirmação", 
            f"Tem certeza que deseja DELETAR o Autor ID {id_valor}?"
        )
        
        if confirmar:
            try:
                self.controlador.gAutor.deletar(id_valor)
                self.limpar_campos()
                self.carregar_dados_iniciais() # Atualiza a tabela
                messagebox.showinfo("Sucesso", f"Autor ID {id_valor} deletado com sucesso!")
            except Exception as e:
                 messagebox.showerror("Erro ao Deletar", f"Não foi possível deletar o autor: {e}")