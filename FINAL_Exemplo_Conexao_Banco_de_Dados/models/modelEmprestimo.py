from .modelConnBD import ModelConnDB
from datetime import date
from classes.emprestimo import Emprestimo

class ModelEmprestimo(ModelConnDB):

    def __init__(self, path_db="/Users/mateuscamilo/Documents/sqlitetestes/gerenciar_biblioteca.db"):
        super().__init__(path_db)
    
    def salvar(self, id_cliente, id_livro, consulta = 'INSERT INTO emprestimo (id_cliente, id_livro) VALUES (?, ?)'):
        return super().salvar(consulta, params=(id_cliente, id_livro))
    
    def deletar(self, id, consulta = 'DELETE FROM emprestimo WHERE id = ?'):
        return super().deletar(consulta, params = (id))
    
    def listar(self, consulta = 'SELECT * FROM emprestimo', params=()):
        dados = super().listar(consulta, params)
        lista_dados = []
        for emprestimo in dados:
            lista_dados.append(self.formatar_emprestimo(emprestimo=emprestimo))
        return lista_dados
    
    def atualizar(self, id, data_efetiva_devolucao=date.today(), consulta = 'UPDATE emprestimo SET data_efetiva_devolucao = ? WHERE id = ?' ):
        return super().atualizar(consulta, params= (data_efetiva_devolucao, id))
    
    def formatar_emprestimo(self, emprestimo):
        id = emprestimo[0]
        data_emprestimo = self.data_em_string(emprestimo[1])
        data_prevista_devolucao = self.data_em_string(emprestimo[2])
        data_efetiva_devolucao = self.data_em_string(emprestimo[3])
        cliente = emprestimo[4]
        livro = emprestimo[5]
        return Emprestimo(id=id, livro=livro, cliente=cliente,data_emprestimo=data_emprestimo, data_efetiva_devolucao=data_efetiva_devolucao, data_prevista_devolucao=data_prevista_devolucao)