from .modelConnBD import ModelConnDB
from classes.livro import Livro # Importação mantida, mas não utilizada no retorno de listar()

class ModelLivro(ModelConnDB):
    
    def __init__(self, path_db="/Users/mateuscamilo/Documents/sqlitetestes/gerenciar_biblioteca.db"):
        super().__init__(path_db)

    def salvar(self, autor, titulo_livro, ISBN, ano_publicacao, consulta = 'INSERT INTO livros (id_autor, titulo_livro, ISBN, ano_publicacao) VALUES (?, ?, ?, ?)'):
        ano_publicacao_formatado = self.string_em_data(ano_publicacao)
        return super().salvar(consulta, params=(autor, titulo_livro, ISBN, ano_publicacao_formatado))
    
    def listar(self, consulta = 'SELECT * FROM livros', params=()):
        dados = super().listar(consulta, params)
        lista_livros_formatada = []
        for livro_tupla in dados:
            # Chama o método de formatação para retornar um DICIONÁRIO
            lista_livros_formatada.append(self.formatar_livro(livro=livro_tupla))
        return lista_livros_formatada
    
    def deletar(self, id, consulta = 'DELETE FROM livros WHERE id = ?'):
        return super().deletar(consulta, params = (id))
    
    # CORREÇÃO NA CONSULTA SQL: Removido parênteses e adicionado o valor de ano_publicacao
    def atualizar(self, id, autor, titulo_livro, ISBN, ano_publicacao, is_emprestado, 
                  consulta = 'UPDATE livros SET id_autor = ?, titulo_livro = ?, ISBN = ?, is_emprestado = ?, ano_publicacao = ? WHERE id = ?'):
        
        ano_publicacao_formatado = self.string_em_data(ano_publicacao)
        # 6 parâmetros (autor, titulo_livro, ISBN, is_emprestado, ano_publicacao_formatado, id) para 6 '?'
        return super().atualizar(consulta, params = (autor, titulo_livro, ISBN, is_emprestado, ano_publicacao_formatado, id))
    
    # MÉTODO ATUALIZADO PARA RETORNAR DICIONÁRIO
    def formatar_livro(self, livro):
        """
        Formata a tupla de dados do banco de dados em um DICIONÁRIO
        para ser consumido pela View (Treeview).
        """
        # A tupla 'livro' é: (id, titulo_livro, isbn, ano_publicacao_str, is_emprestado, id_autor)
        id = livro[0]
        titulo_livro = livro[1]
        isbn = livro[2]
        ano_publicacao = self.data_em_string(livro[3]) # Converte de volta para string legível
        is_emprestado = livro[4]
        id_autor = livro[5]
        
        # O RETORNO é um dicionário
        return {
            "id": id,
            "id_autor": id_autor,
            "titulo_livro": titulo_livro,
            "ISBN": isbn,
            "ano_publicacao": ano_publicacao,
            "is_emprestado": is_emprestado
        }
    