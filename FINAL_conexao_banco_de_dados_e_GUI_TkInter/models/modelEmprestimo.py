from .modelConnBD import ModelConnDB
from datetime import date
from classes.emprestimo import Emprestimo # Importação mantida, mas não utilizada no retorno de listar()

class ModelEmprestimo(ModelConnDB):

    def __init__(self, path_db="/Users/mateuscamilo/Documents/sqlitetestes/gerenciar_biblioteca.db"):
        super().__init__(path_db)
    
    def salvar(self, id_cliente, id_livro, consulta = 'INSERT INTO emprestimo (id_cliente, id_livro) VALUES (?, ?)'):
        return super().salvar(consulta, params=(id_cliente, id_livro))
    
    def deletar(self, id, consulta = 'DELETE FROM emprestimo WHERE id = ?'):
        return super().deletar(consulta, params = (id))
    
    def listar(self, consulta = 'SELECT * FROM emprestimo', params=()):
        dados = super().listar(consulta, params)
        lista_dados_formatada = []
        for emprestimo_tupla in dados:
            # Chama o método de formatação para retornar um DICIONÁRIO
            lista_dados_formatada.append(self.formatar_emprestimo(emprestimo=emprestimo_tupla))
        return lista_dados_formatada
    
    def atualizar(self, id, data_efetiva_devolucao=date.today(), consulta = 'UPDATE emprestimo SET data_efetiva_devolucao = ? WHERE id = ?' ):
        # Formata a data de devolução (que é um objeto date) para string no formato do BD
        data_devolucao_formatada = self.string_em_data(data_efetiva_devolucao)
        return super().atualizar(consulta, params= (data_devolucao_formatada, id))
    
    # MÉTODO ATUALIZADO PARA RETORNAR DICIONÁRIO
    def formatar_emprestimo(self, emprestimo):
        """
        Formata a tupla de dados do banco de dados em um DICIONÁRIO
        para ser consumido pela View (Treeview).
        """
        id = emprestimo[0]
        data_emprestimo = self.data_em_string(emprestimo[1])
        data_prevista_devolucao = self.data_em_string(emprestimo[2])
        data_efetiva_devolucao = self.data_em_string(emprestimo[3])
        cliente = emprestimo[4]
        livro = emprestimo[5]
        
        # O RETORNO é um dicionário, que a View espera
        return {
            "id": id,
            "id_livro": livro,
            "id_cliente": cliente,
            "data_emprestimo": data_emprestimo,
            "data_prevista_devolucao": data_prevista_devolucao,
            "data_efetiva_devolucao": data_efetiva_devolucao
        }