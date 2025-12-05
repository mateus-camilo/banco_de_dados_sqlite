from flask import Flask, render_template, request, url_for, redirect
import crud_models as db # Importa o módulo com as funções CRUD da biblioteca
from datetime import date # Para data de devolução

# Configuração da aplicação Flask
app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

# --- ROTAS PRINCIPAIS ---

@app.route("/")
def index():
    """
    Rota inicial que serve como dashboard/menu.
    Lista clientes para exibição rápida na página inicial.
    """
    clientes = db.listar_clientes() 
    return render_template("index.html", clientes=clientes)

# --- ROTAS CRUD PARA CLIENTES ---

@app.route("/clientes")
def listar_clientes_route():
    """Exibe o formulário de cadastro e a lista de clientes."""
    clientes = db.listar_clientes()
    return render_template("clientes.html", clientes=clientes)

@app.route("/clientes/adicionar", methods=['POST'])
def adicionar_cliente():
    """Adiciona um novo cliente."""
    nome = request.form.get('nome')
    email = request.form.get('email')
    data_nascimento = request.form.get('data_nascimento')
    
    if nome and email:
        db.salvar_cliente(nome, email, data_nascimento)
    
    return redirect(url_for('listar_clientes_route'))

@app.route("/clientes/editar/<int:id>", methods=['GET', 'POST'])
def editar_cliente(id):
    """Exibe o formulário preenchido para edição ou processa a atualização."""
    cliente = db.buscar_cliente_por_id(id)
    
    if cliente is None:
        return redirect(url_for('listar_clientes_route'))
        
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        data_nascimento = request.form.get('data_nascimento')
        
        if nome and email:
            db.atualizar_cliente(id, nome, email, data_nascimento)
        
        return redirect(url_for('listar_clientes_route'))
    
    return render_template('clientes_editar.html', cliente=cliente)

@app.route("/clientes/deletar/<int:id>", methods=['POST'])
def deletar_cliente_route(id):
    """Deleta um cliente."""
    db.deletar_cliente(id)
    return redirect(url_for('listar_clientes_route'))

# --- ROTAS CRUD PARA AUTORES ---

@app.route("/autores")
def listar_autores_route():
    autores = db.listar_autores()
    return render_template("autores.html", autores=autores)

@app.route("/autores/adicionar", methods=['POST'])
def adicionar_autor():
    nome = request.form.get('nome')
    data_nascimento = request.form.get('data_nascimento')
    biografia = request.form.get('biografia')
    if nome:
        db.salvar_autor(nome, data_nascimento, biografia)
    return redirect(url_for('listar_autores_route'))

@app.route("/autores/editar/<int:id>", methods=['GET', 'POST'])
def editar_autor(id):
    autor = db.buscar_autor_por_id(id)
    if autor is None:
        return redirect(url_for('listar_autores_route'))
        
    if request.method == 'POST':
        nome = request.form.get('nome')
        data_nascimento = request.form.get('data_nascimento')
        biografia = request.form.get('biografia')
        if nome:
            db.atualizar_autor(id, nome, data_nascimento, biografia)
        return redirect(url_for('listar_autores_route'))
    
    return render_template('autores_editar.html', autor=autor)

@app.route("/autores/deletar/<int:id>", methods=['POST'])
def deletar_autor_route(id):
    db.deletar_autor(id)
    return redirect(url_for('listar_autores_route'))
    
# --- ROTAS CRUD PARA LIVROS ---

@app.route("/livros")
def listar_livros_route():
    livros = db.listar_livros()
    autores = db.listar_autores() # Necessário para o dropdown de ID do Autor
    return render_template("livros.html", livros=livros, autores=autores)

@app.route("/livros/adicionar", methods=['POST'])
def adicionar_livro():
    id_autor = request.form.get('id_autor')
    titulo_livro = request.form.get('titulo_livro')
    ISBN = request.form.get('ISBN')
    ano_publicacao = request.form.get('ano_publicacao')
    if titulo_livro and id_autor:
        db.salvar_livro(id_autor, titulo_livro, ISBN, ano_publicacao)
    return redirect(url_for('listar_livros_route'))

@app.route("/livros/editar/<int:id>", methods=['GET', 'POST'])
def editar_livro_route(id):
    livro = db.buscar_livro_por_id(id)
    autores = db.listar_autores()
    if livro is None:
        return redirect(url_for('listar_livros_route'))
        
    if request.method == 'POST':
        id_autor = request.form.get('id_autor')
        titulo_livro = request.form.get('titulo_livro')
        ISBN = request.form.get('ISBN')
        ano_publicacao = request.form.get('ano_publicacao')
        is_emprestado = request.form.get('is_emprestado', 0) # Pega o status, default 0
        if titulo_livro and id_autor:
            db.atualizar_livro(id, id_autor, titulo_livro, ISBN, ano_publicacao, is_emprestado)
        return redirect(url_for('listar_livros_route'))
    
    return render_template('livros_editar.html', livro=livro, autores=autores)

@app.route("/livros/deletar/<int:id>", methods=['POST'])
def deletar_livro_route(id):
    db.deletar_livro(id)
    return redirect(url_for('listar_livros_route'))

# --- ROTAS CRUD PARA EMPRÉSTIMOS ---

@app.route("/emprestimos")
def listar_emprestimos_route():
    emprestimos = db.listar_emprestimos()
    clientes = db.listar_clientes() # Para o formulário de novo empréstimo
    livros_disp = [l for l in db.listar_livros() if l['is_emprestado'] == 0] # Livros disponíveis
    return render_template("emprestimos.html", emprestimos=emprestimos, clientes=clientes, livros_disp=livros_disp)

@app.route("/emprestimos/iniciar", methods=['POST'])
def iniciar_emprestimo():
    id_cliente = request.form.get('id_cliente')
    id_livro = request.form.get('id_livro')
    
    if id_cliente and id_livro:
        db.salvar_emprestimo(id_cliente, id_livro)
    
    return redirect(url_for('listar_emprestimos_route'))

@app.route("/emprestimos/devolver/<int:id>/<int:id_livro>/<int:id_cliente>", methods=['POST'])
def devolver_emprestimo(id, id_livro, id_cliente):
    # A data de devolução é a data de hoje
    data_efetiva = date.today().strftime('%Y-%m-%d')
    db.devolver_livro(id, data_efetiva, id_livro, id_cliente)
    return redirect(url_for('listar_emprestimos_route'))


if __name__ == '__main__':
    app.run()