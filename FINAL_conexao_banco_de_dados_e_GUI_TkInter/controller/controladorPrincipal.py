from views.autor_view import TelaAutor
from views.cliente_view import TelaCliente
from views.emprestimo_view import TelaEmprestimo
from views.livro_view import TelaLivro
from views.menu_lateral_view import TelaMenuLateral
from controller.controladorModels import ControladorModels
import tkinter as tk

class ControladorPrincipal:

    def __init__(self):
        self.controladorModel = ControladorModels()
        self.criar_tela_principal()

    def criar_tela_principal(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Gerenciamento de Biblioteca")
        self.root.geometry("1000x600") 
    
        # 1. Cria o frame principal que conterá o menu e o conteúdo
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)
    
        # 2. Configura a grade (grid) para as proporções: 20% e 80%
        # A coluna 0 (Menu) terá peso 2 (20%)
        self.main_frame.grid_columnconfigure(0, weight=2)
        # A coluna 1 (Conteúdo) terá peso 8 (80%)
        self.main_frame.grid_columnconfigure(1, weight=8)
        # A linha 0 ocupa 100% da altura
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.tela_menu_lateral = TelaMenuLateral(master=self.main_frame, controlador=self)
        self.tela_menu_lateral.grid(row=0, column=0, sticky="nsew")
        self.event_bt_inicio()

    def destruir_widgets_na_coluna(self, frame_pai, coluna_alvo=1):
        """
        Destrói todos os widgets filhos de um Frame que estão
        posicionados na coluna específica do gerenciador Grid.
        """
        # Itera sobre todos os widgets que são filhos diretos do frame_pai
        for widget in frame_pai.winfo_children():
            
            # O menu lateral está na coluna 0, queremos ignorá-lo
            if widget.winfo_manager() == 'grid':
                info = widget.grid_info()
                
                # Verifica se o widget está na coluna alvo (padrão é 1, a área de conteúdo)
                if 'column' in info and info['column'] == coluna_alvo:
                    widget.destroy()

    def destruir_conteudo_principal(self):
        """Chama a função utilitária para limpar a coluna 1."""
        # Chamamos a função com o frame pai (main_frame) e a coluna 1 (conteúdo)
        self.destruir_widgets_na_coluna(self.main_frame, coluna_alvo=1)
        
    def carregar_tela(self, NovaTela, controlador_model):
        """Destrói o conteúdo atual e carrega a nova Tela selecionada dentro da coluna 1."""
        self.destruir_conteudo_principal()
        
        # Instancia e posiciona o novo Frame (CRUDFrameCliente, por exemplo)
        nova_tela = NovaTela(controlador=controlador_model, master=self.main_frame)
        nova_tela.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    def event_bt_inicio(self):
        """Carrega a tela inicial."""
        # Simulando uma tela inicial simples
        class TelaInicial(tk.Frame):
            def __init__(self, master=None, controlador=self):
                super().__init__(master=master)
                self.controlador = controlador
        self.carregar_tela(TelaInicial, controlador_model=self.controladorModel)

    def event_bt_clientes(self):
        """Carrega o CRUD de Clientes."""
        self.carregar_tela(TelaCliente, controlador_model=self.controladorModel)

    def event_bt_autores(self):
        """Carrega o CRUD de Autores."""
        self.carregar_tela(TelaAutor, controlador_model=self.controladorModel)

    def event_bt_livros(self):
        """Carrega o CRUD de Livros."""
        self.carregar_tela(TelaLivro, controlador_model=self.controladorModel)

    def event_bt_emprestimos(self):
        """Carrega o CRUD de Empréstimos."""
        self.carregar_tela(TelaEmprestimo, controlador_model=self.controladorModel)