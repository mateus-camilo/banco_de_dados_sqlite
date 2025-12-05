from pydantic import BaseModel
from classes.pessoa.autor import Autor
from datetime import date

class Livro(BaseModel):
    id:int
    autor:Autor | int
    titulo_livro:str
    ISBN: str
    ano_publicacao:date |str
    is_emprestado : bool

    def __str__(self):
        return (f'''Título do livro: {self.titulo_livro}\n
                Autor: {self.autor}\n
                ISBN: {self.ISBN}\n
                Ano de publicação: {self.ano_publicacao}\n
                Status: {'emprestado' if self.is_emprestado else 'disponível'}\n
                 ''')

