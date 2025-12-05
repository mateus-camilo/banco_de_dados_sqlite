from .modelConnBD import ModelConnDB
from classes.pessoa.cliente import Cliente # Importação mantida, mas não utilizada no retorno de listar()

class ModelCliente(ModelConnDB):

    def __init__(self, path_db="/Users/mateuscamilo/Documents/sqlitetestes/gerenciar_biblioteca.db"):
        super().__init__(path_db)
    
    def salvar(self, email, nome, data_nascimento, consulta="INSERT INTO clientes (email, nome, data_nascimento) VALUES (?, ?, ?)"):
        data_nascimento = self.string_em_data(data_nascimento)
        return super().salvar(consulta, params = (email, nome, data_nascimento))
    
    def atualizar(self,  email, nome, data_nascimento, id, consulta = "UPDATE clientes SET email = ?, nome = ?, data_nascimento = ? WHERE id = ?"):
        data_nascimento = self.string_em_data(data_nascimento)
        return super().atualizar(consulta, params = (email, nome, data_nascimento, id))
    
    def deletar(self, id, consulta = 'DELETE FROM clientes WHERE id = ?'):
        return super().deletar(consulta, params = (id))
    
    def listar(self, consulta = 'SELECT * FROM clientes', params=()):
        dados = super().listar(consulta, params)
        lista_clientes_formatada = []
        for cliente_tupla in dados:
            # Chama o método de formatação para retornar um DICIONÁRIO
            lista_clientes_formatada.append(self.formatar_cliente(cliente=cliente_tupla))
        return lista_clientes_formatada
    
    # MÉTODO ATUALIZADO PARA RETORNAR DICIONÁRIO
    def formatar_cliente(self, cliente):
        """
        Formata a tupla de dados do banco de dados em um DICIONÁRIO
        para ser consumido pela View (Treeview).
        """
        # A tupla 'cliente' é: (id, email, nome, data_nascimento_str, total_emprestimo)
        id = cliente[0]
        email = cliente[1]
        nome = cliente[2]
        data_nascimento = self.data_em_string(cliente[3]) # Converte de volta para string legível
        total_emprestimo = cliente[4]
        
        # O RETORNO é um dicionário
        return {
            "id": id,
            "email": email,
            "nome": nome,
            "data_nascimento": data_nascimento,
            "total_emprestimo": total_emprestimo
        }