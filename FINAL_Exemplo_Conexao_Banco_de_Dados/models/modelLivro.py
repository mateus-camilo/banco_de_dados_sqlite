from .modelConnBD import ModelConnDB
from classes.livro import Livro
class ModelLivro(ModelConnDB):
    
    def __init__(self, path_db="/Users/mateuscamilo/Documents/sqlitetestes/gerenciar_biblioteca.db"):
        super().__init__(path_db)

    def salvar(self, autor, titulo_livro, ISBN, ano_publicacao, consulta = 'INSERT INTO livros (id_autor, titulo_livro, ISBN, ano_publicacao)'
    'VALUES (?, ?, ?, ?)'):
        ano_publicacao_formatado = self.string_em_data(ano_publicacao)
        return super().salvar(consulta, params=(autor, titulo_livro, ISBN, ano_publicacao_formatado))
    
    def listar(self, consulta = 'SELECT * FROM livros', params=()):
        dados = super().listar(consulta, params)
        lista_livros = []
        for livro in dados:
            lista_livros.append(self.formatar_livro(livro=livro))
        return lista_livros
    
    def deletar(self, id, consulta = 'DELETE FROM livros WHERE id = ?'):
        return super().deletar(consulta, params = (id))
    
    def atualizar(self, id, autor, titulo_livro, ISBN, ano_publicacao, is_emprestado, consulta = 'UPDATE livros SET (id_autor = ?, titulo_livro = ?, ISBN = ?, is_emprestado = ?, ano_publicacao) WHERE id = ?'):
        ano_publicacao_formatado = self.string_em_data(ano_publicacao)
        return super().atualizar(consulta, params = (autor, titulo_livro, ISBN, is_emprestado, ano_publicacao_formatado, id))
    
    def formatar_livro(self, livro):
        id = livro[0]
        titulo_livro = livro[1]
        isbn = livro[2]
        ano_publicacao = self.data_em_string(livro[3])
        is_emprestado = livro[4]
        id_autor = livro[5]
        return Livro(id=id, autor=id_autor, titulo_livro=titulo_livro, ISBN=isbn, ano_publicacao=ano_publicacao, is_emprestado=is_emprestado)