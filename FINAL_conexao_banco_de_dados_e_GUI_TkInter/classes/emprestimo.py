from pydantic import BaseModel
from classes.livro import Livro
from classes.pessoa.cliente import Cliente
from datetime import date

class Emprestimo(BaseModel):
    id:int
    livro:Livro | int
    cliente:Cliente |int
    data_emprestimo:date | str 
    data_prevista_devolucao:date | str
    data_efetiva_devolucao:date | str | None

    def __str__(self):
        return (f"""
                Identificador único: {self.id}\n
                Livro: {self.livro}\n
                Cliente: {self.cliente}\n
                Data de empréstimo: {self.data_emprestimo}\n
                Data prevista de devolução: {self.data_prevista_devolucao}\n
                Data efetiva da devolução: {self.data_efetiva_devolucao if self.data_efetiva_devolucao else 'Não devolveu'}\n
                """)