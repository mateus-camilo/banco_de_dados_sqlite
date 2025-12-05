from .modelConnBD import ModelConnDB
from classes.pessoa.autor import Autor

class ModelAutor(ModelConnDB):

    def __init__(self, path_db="/Users/mateuscamilo/Documents/sqlitetestes/gerenciar_biblioteca.db"):
        super().__init__(path_db)

    def salvar(self, nome, data_nascimento, biografia, consulta= 'INSERT INTO autor (nome, data_nascimento, biografia) VALUES (?, ?, ?)'):
        data_nascimento = self.string_em_data(data_nascimento)
        return super().salvar(consulta, params=(nome, data_nascimento, biografia))
    
    def deletar(self, id, consulta = 'DELETE FROM autor WHERE id = ?'):
        return super().deletar(consulta, params = (id))
    
    def atualizar(self, id, nome, data_nascimento, biografia, consulta = 'UPDATE autor SET nome = ?, data_nascimento = ?, biografia = ? WHERE id = ?'):
        return super().atualizar(consulta, params = (nome, data_nascimento, biografia, id))
    
    def listar(self, consulta = 'SELECT * FROM autor', params=()):
        dados = super().listar(consulta, params)
        lista_autores = []
        for autor in dados:
            lista_autores.append(self.formatar_autor(autor=autor))
        return lista_autores
    
    def formatar_autor(self, autor):
        id = autor[0]
        nome = autor[1]
        data_nascimento = self.data_em_string(autor[2])
        biografia = autor[3]
        return Autor(id=id, nome=nome, data_nascimento=data_nascimento, biografia=biografia)