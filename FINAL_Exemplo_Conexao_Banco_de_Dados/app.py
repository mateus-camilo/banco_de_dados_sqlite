from controller.controlador import Controlador

if __name__ == "__main__":
    controle = Controlador()
    
    controle.listar_info(controle.gAutor.listar())
    controle.listar_info(controle.gCliente.listar())
    controle.listar_info(controle.gLivro.listar())
    controle.listar_info(controle.gEmprestimo.listar())
