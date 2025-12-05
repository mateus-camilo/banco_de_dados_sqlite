from classes.pessoa.pessoa import Pessoa
from pydantic import EmailStr

class Cliente(Pessoa):

    email : EmailStr
    total_emprestimo : int

    def __str__(self):
        return (f"""
                Identificador único: {self.id}\n
                Cliente: {self.nome}\n
                E-mail: {self.email}\n
                Data de nascimento: {self.data_nascimento}\n
                Total de empréstimo: {self.total_emprestimo}\n
                """)