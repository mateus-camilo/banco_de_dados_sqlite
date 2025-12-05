from models.modelCliente import ModelCliente
from models.modelLivro import ModelLivro
from models.modelEmprestimo import ModelEmprestimo
from models.modelAutor import ModelAutor

class ControladorModels:

    def __init__(self):
        self.gCliente = ModelCliente()
        self.gAutor = ModelAutor()
        self.gLivro = ModelLivro()
        self.gEmprestimo = ModelEmprestimo()

    def listar_info(self, lista_dados):
        for dado in lista_dados:
            print(dado)

