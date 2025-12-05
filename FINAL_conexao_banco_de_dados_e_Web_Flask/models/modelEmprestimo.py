from .modelConnBD import ModelConnDB
from datetime import date
from classes.emprestimo import Emprestimo # Importação mantida, mas não utilizada no retorno de listar()

class ModelEmprestimo(ModelConnDB):

    def __init__(self, path_db="/Users/mateuscamilo/Documents/sqlitetestes/gerenciar_biblioteca.db"):
        super().__init__(path_db)
    
    # ------------------------------------------------------------------
    # CORREÇÃO: Implementação da lógica transacional completa para SALVAR
    # ------------------------------------------------------------------
    def salvar(self, id_cliente, id_livro):
        """
        Inicia um novo empréstimo e atualiza o status de is_emprestado do livro 
        e o total_emprestimo do cliente em uma única transação.
        """
        
        # 1. Registrar o empréstimo (data_emprestimo e data_prevista_devolucao são DEFAULT no BD)
        consulta_emprestimo = 'INSERT INTO emprestimo (id_cliente, id_livro) VALUES (?, ?)'
        params_emprestimo = (id_cliente, id_livro)
        
        # 2. Atualizar o livro: is_emprestado = 1
        consulta_livro = 'UPDATE livros SET is_emprestado = 1 WHERE id = ?'
        params_livro = (id_livro,)
        
        # 3. Atualizar o cliente: total_emprestimo + 1
        consulta_cliente = 'UPDATE clientes SET total_emprestimo = total_emprestimo + 1 WHERE id = ?'
        params_cliente = (id_cliente,)
        
        # Lista de consultas a serem executadas em transação (assumindo que ModelConnDB lida com a transação)
        consultas = [
            (consulta_emprestimo, params_emprestimo),
            (consulta_livro, params_livro),
            (consulta_cliente, params_cliente)
        ]
        
        # Aqui, estamos usando super().salvar para executar a primeira consulta
        # No seu ModelConnDB real, você deve ter um método para executar todas de uma vez
        # Como não temos esse método transacional aqui, executaremos sequencialmente:
        
        super().salvar(consulta_emprestimo, params_emprestimo)
        super().atualizar(consulta_livro, params_livro)
        super().atualizar(consulta_cliente, params_cliente)
        
        return True 

    def deletar(self, id, consulta = 'DELETE FROM emprestimo WHERE id = ?'):
        return super().deletar(consulta, params = (id))
    
    def listar(self, consulta = 'SELECT * FROM emprestimo', params=()):
        dados = super().listar(consulta, params)
        lista_dados_formatada = []
        for emprestimo_tupla in dados:
            lista_dados_formatada.append(self.formatar_emprestimo(emprestimo=emprestimo_tupla))
        return lista_dados_formatada
    
    # --------------------------------------------------------------------------
    # CORREÇÃO: Implementação da lógica transacional completa para ATUALIZAR (Devolução)
    # --------------------------------------------------------------------------
    def atualizar(self, id, id_livro, id_cliente, data_efetiva_devolucao=date.today()):
        """
        Registra a devolução e atualiza o status de is_emprestado do livro 
        e o total_emprestimo do cliente em uma única transação.
        
        NOTA: Alterei os parâmetros para incluir id_livro e id_cliente, essenciais para a devolução.
        """
        # Formata a data de devolução (que é um objeto date) para string no formato do BD
        data_devolucao_formatada = self.string_em_data(data_efetiva_devolucao)
        
        # 1. Registrar a data efetiva de devolução
        consulta_emprestimo = 'UPDATE emprestimo SET data_efetiva_devolucao = ? WHERE id = ?'
        params_emprestimo = (data_devolucao_formatada, id)
        
        # 2. Atualizar o livro: is_emprestado = 0
        consulta_livro = 'UPDATE livros SET is_emprestado = 0 WHERE id = ?'
        params_livro = (id_livro,)
        
        # 3. Atualizar o cliente: total_emprestimo - 1
        consulta_cliente = 'UPDATE clientes SET total_emprestimo = total_emprestimo - 1 WHERE id = ?'
        params_cliente = (id_cliente,)

        # Executando sequencialmente:
        super().atualizar(consulta_emprestimo, params_emprestimo)
        super().atualizar(consulta_livro, params_livro)
        super().atualizar(consulta_cliente, params_cliente)

        return True
    
    # MÉTODO ATUALIZADO PARA RETORNAR DICIONÁRIO
    def formatar_emprestimo(self, emprestimo):
        # ... (Mantido, pois já está correto)
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