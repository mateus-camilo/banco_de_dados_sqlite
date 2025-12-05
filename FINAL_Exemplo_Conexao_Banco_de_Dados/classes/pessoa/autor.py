from classes.pessoa.pessoa import Pessoa

class Autor(Pessoa):

    biografia : str

    def __str__(self):
        return (f"""
                Identificador único: {self.id}\n
                Autor: {self.nome}\n
                data de nascimento: {self.data_nascimento}\n
                biografia: {self.biografia}
""")