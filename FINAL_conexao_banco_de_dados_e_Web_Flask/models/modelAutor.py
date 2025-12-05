from .modelConnBD import ModelConnDB
from classes.pessoa.autor import Autor # Importação mantida, mas não utilizada no retorno

class ModelAutor(ModelConnDB):

    def __init__(self, path_db="/Users/mateuscamilo/Documents/sqlitetestes/gerenciar_biblioteca.db"):
        super().__init__(path_db)

    def salvar(self, nome, data_nascimento, biografia, consulta= 'INSERT INTO autor (nome, data_nascimento, biografia) VALUES (?, ?, ?)'):
        data_nascimento = self.string_em_data(data_nascimento)
        return super().salvar(consulta, params=(nome, data_nascimento, biografia))
    
    def deletar(self, id, consulta = 'DELETE FROM autor WHERE id = ?'):
        return super().deletar(consulta, params = (id))
    
    def atualizar(self, id, nome, data_nascimento, biografia, consulta = 'UPDATE autor SET nome = ?, data_nascimento = ?, biografia = ? WHERE id = ?'):
        data_nascimento = self.string_em_data(data_nascimento) # Convertendo data para o formato do BD
        return super().atualizar(consulta, params = (nome, data_nascimento, biografia, id))
    
    def listar(self, consulta = 'SELECT * FROM autor', params=()):
        dados = super().listar(consulta, params)
        lista_autores_formatada = []
        for autor_tupla in dados:
            # Chama o método de formatação para retornar um DICIONÁRIO
            lista_autores_formatada.append(self.formatar_autor(autor=autor_tupla))
        return lista_autores_formatada
    
    def formatar_autor(self, autor):
        """
        Formata a tupla de dados do banco de dados em um DICIONÁRIO
        para ser consumido pela View (Treeview).
        """
        # A tupla 'autor' é: (id, nome, data_nascimento_str, biografia)
        id = autor[0]
        nome = autor[1]
        data_nascimento = self.data_em_string(autor[2]) # Converte de volta para string legível
        biografia = autor[3]
        
        # O RETORNO é um dicionário, que a View espera
        return {
            "id": id,
            "nome": nome,
            "data_nascimento": data_nascimento,
            "biografia": biografia
        }