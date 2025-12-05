import tkinter as tk
from tkinter import ttk

class TelaMenuLateral(tk.Frame):
    """Frame que contém o menu lateral e os botões de navegação."""
    def __init__(self, master=None, controlador =None):
        super().__init__(master, bg='#2c3e50') # Cor de fundo escura para menu
        self.controlador = controlador
        self.botoes = {
            "Início": "event_bt_inicio",
            "Clientes": "event_bt_clientes",
            "Autores": "event_bt_autores",
            "Livros": "event_bt_livros",
            "Empréstimos": "event_bt_emprestimos",
        }
        
        self._criar_botoes()

    def _criar_botoes(self):
        """Cria e empacota os botões dentro do menu lateral."""
        
        # Cria um título para o menu
        titulo = ttk.Label(self, text="MENU", 
                           foreground="white", 
                           background=self['bg'],
                           font=("Arial", 14, "bold"))
        titulo.pack(pady=(20, 10), padx=10, fill='x')

        for texto, comando_nome in self.botoes.items():
            # Estilo para os botões do menu
            btn = ttk.Button(self, text=texto, command= lambda evento=comando_nome: self.chamar_tela(evento))
            
            # Preenche a largura do frame do menu, adiciona padding
            btn.pack(fill='x', padx=10, pady=5)
    
    def chamar_tela(self, nome_event):
        if nome_event=="event_bt_inicio":
            print('Dentro do if 1')
            return self.controlador.event_bt_inicio()
        elif nome_event == "event_bt_clientes":
            print('Dentro do if 2')
            return self.controlador.event_bt_clientes()
        elif nome_event == "event_bt_autores":
            print('Dentro do if 3')
            return self.controlador.event_bt_autores()
        elif nome_event == "event_bt_livros":
            print('Dentro do if 4')
            return self.controlador.event_bt_livros()
        elif nome_event == "event_bt_emprestimos":
            print('Dentro do if 5')
            return self.controlador.event_bt_emprestimos()
    
