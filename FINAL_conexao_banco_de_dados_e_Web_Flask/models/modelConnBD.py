import sqlite3
from datetime import date

class ModelConnDB:

    def __init__(self, path_db="/Users/mateuscamilo/Documents/sqlitetestes/gerenciar_biblioteca.db"):
        self.path_db = path_db
        self._criar_esquema_tabelas()

    def _executar_query(self, consulta, params = ()):
        with sqlite3.connect(self.path_db) as conn:
            cursor = conn.cursor()
            cursor.execute(consulta, params)

            if(consulta.lower().split()[0] == 'select'):
                return cursor.fetchall()
            else:
                return cursor.rowcount   
             
    def _criar_esquema_tabelas(self):
        with sqlite3.connect(self.path_db) as conn:
            cursor = conn.cursor()
            cursor.executescript(self.criar_tabelas())
                
    def salvar(self, consulta, params = ()):
        return self._executar_query(consulta, params)
    
    def deletar(self, consulta, params = ()):
        return self._executar_query(consulta, params)
    
    def listar(self, consulta, params = ()):
        return self._executar_query(consulta, params)
    
    def atualizar(self, consulta, params = ()):
        return self._executar_query(consulta, params)
    
    def criar_tabelas(self):
        consulta_tabelas = ("""
                            PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS clientes(
                            id INTEGER PRIMARY KEY,
                            email TEXT UNIQUE NOT NULL,
                            nome TEXT NOT NULL,
                            data_nascimento DATE,
                            total_emprestimo INTEGER DEFAULT 0
                            );
        
        CREATE TABLE IF NOT EXISTS autor(
                            id INTEGER PRIMARY KEY,
                            nome TEXT NOT NULL,
                            data_nascimento DATE,
                            biografia TEXT
                            );

        CREATE TABLE IF NOT EXISTS livros(
                            id INTEGER PRIMARY KEY,
                            titulo_livro TEXT NOT NULL,
                            ISBN TEXT NOT NULL,
                            ano_publicacao DATE NOT NULL,
                            is_emprestado INTEGER DEFAULT 0,
                            id_autor INTEGER NOT NULL,
                            FOREIGN KEY (id_autor) REFERENCES autor (id)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE
                            );

        CREATE TABLE IF NOT EXISTS emprestimo(
                            id INTEGER PRIMARY KEY,
                            data_emprestimo DATE DEFAULT (date('now', 'utc', '-3 hours')),
                            data_prevista_devolucao DATE DEFAULT (date('now', 'utc', '-3 hours', '+7 days')),
                            data_efetiva_devolucao DATE DEFAULT NULL,
                            id_cliente INTEGER NOT NULL,
                            id_livro INTEGER NOT NULL,
                    FOREIGN KEY (id_cliente) REFERENCES clientes (id)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE,
                    FOREIGN KEY (id_livro) REFERENCES livros (id)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE
                            );  
""")
        return consulta_tabelas
    
    def string_em_data(self, data:str):
        if data is None:
            return None
        data_formatada = date.strptime(data, '%d/%m/%Y')
        return data_formatada
    
    def data_em_string(self, data:date):
        if data is None:
            return None
        objeto_data = date.fromisoformat(data)
        data_formatada = objeto_data.strftime('%d/%m/%Y')
        return data_formatada

                