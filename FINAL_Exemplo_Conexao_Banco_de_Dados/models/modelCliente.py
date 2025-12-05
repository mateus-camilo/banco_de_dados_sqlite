from .modelConnBD import ModelConnDB
from classes.pessoa.cliente import Cliente

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
        lista_clientes = []
        for cliente in dados:
            lista_clientes.append(self.formatar_cliente(cliente=cliente))
        return lista_clientes
    
    def formatar_cliente(self, cliente):
        id = cliente[0]
        email = cliente[1]
        nome = cliente[2]
        data_nascimento = self.data_em_string(cliente[3])
        total_emprestimo = cliente[4]
        return Cliente(id=id, nome=nome, data_nascimento=data_nascimento, email=email, total_emprestimo=total_emprestimo)