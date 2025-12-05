import sqlite3
from datetime import date

# ATENÇÃO: SUBSTITUA PELO SEU CAMINHO CORRETO DO BANCO DE DADOS
DB_PATH = "/Users/mateuscamilo/Documents/sqlitetestes/gerenciar_biblioteca.db"

# --- Funções de Conexão e Query ---

def _executar_query(consulta: str, params = ()):
    """
    Executa uma consulta SQL genérica e retorna dados como dicionário.
    Lida com transações (COMMIT/ROLLBACK).
    """
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        
        try:
            cursor.execute(consulta, params)
            
            verificar_tipo_consulta = consulta.lower().split()[0]
            if verificar_tipo_consulta == 'select':
                # Retorna lista de dicionários
                return [dict(row) for row in cursor.fetchall()]
            else:
                conn.commit()
                return cursor.rowcount
        except Exception as e:
            conn.rollback()
            print(f"Erro na transação SQL: {e}")
            raise e
        finally:
             cursor.close()

# --- Funções CRUD Específicas para Cliente ---

def listar_clientes():
    """Lista todos os clientes."""
    return _executar_query('SELECT id, nome, email, data_nascimento, total_emprestimo FROM clientes')

def salvar_cliente(nome, email, data_nascimento):
    """Salva um novo cliente."""
    consulta = 'INSERT INTO clientes (nome, email, data_nascimento) VALUES (?, ?, ?)'
    return _executar_query(consulta, (nome, email, data_nascimento))

def buscar_cliente_por_id(id):
    """Busca um cliente específico por ID."""
    dados = _executar_query('SELECT id, nome, email, data_nascimento, total_emprestimo FROM clientes WHERE id = ?', (id,))
    return dados[0] if dados else None

def atualizar_cliente(id, nome, email, data_nascimento):
    """Atualiza dados de um cliente."""
    consulta = 'UPDATE clientes SET nome = ?, email = ?, data_nascimento = ? WHERE id = ?'
    return _executar_query(consulta, (nome, email, data_nascimento, id))

def deletar_cliente(id):
    """Deleta um cliente por ID."""
    return _executar_query('DELETE FROM clientes WHERE id = ?', (id,))

# --- Funções CRUD Específicas para Autor ---

def listar_autores():
    """Lista todos os autores."""
    return _executar_query('SELECT id, nome, data_nascimento, biografia FROM autor')

def salvar_autor(nome, data_nascimento, biografia):
    """Salva um novo autor."""
    consulta = 'INSERT INTO autor (nome, data_nascimento, biografia) VALUES (?, ?, ?)'
    return _executar_query(consulta, (nome, data_nascimento, biografia))

def buscar_autor_por_id(id):
    """Busca um autor específico por ID."""
    dados = _executar_query('SELECT id, nome, data_nascimento, biografia FROM autor WHERE id = ?', (id,))
    return dados[0] if dados else None

def atualizar_autor(id, nome, data_nascimento, biografia):
    """Atualiza dados de um autor."""
    consulta = 'UPDATE autor SET nome = ?, data_nascimento = ?, biografia = ? WHERE id = ?'
    return _executar_query(consulta, (nome, data_nascimento, biografia, id))

def deletar_autor(id):
    """Deleta um autor por ID."""
    return _executar_query('DELETE FROM autor WHERE id = ?', (id,))

# --- Funções CRUD Específicas para Livro ---

def listar_livros():
    """Lista todos os livros, incluindo o nome do autor."""
    consulta = """
        SELECT l.id, l.titulo_livro, l.ISBN, l.ano_publicacao, l.is_emprestado, l.id_autor, a.nome as nome_autor
        FROM livros l
        LEFT JOIN autor a ON l.id_autor = a.id
    """
    return _executar_query(consulta)

def salvar_livro(id_autor, titulo_livro, ISBN, ano_publicacao):
    """Salva um novo livro."""
    consulta = 'INSERT INTO livros (id_autor, titulo_livro, ISBN, ano_publicacao) VALUES (?, ?, ?, ?)'
    return _executar_query(consulta, (id_autor, titulo_livro, ISBN, ano_publicacao))

def buscar_livro_por_id(id):
    """Busca um livro específico por ID."""
    dados = _executar_query('SELECT id, titulo_livro, ISBN, ano_publicacao, is_emprestado, id_autor FROM livros WHERE id = ?', (id,))
    return dados[0] if dados else None

def atualizar_livro(id, id_autor, titulo_livro, ISBN, ano_publicacao, is_emprestado):
    """Atualiza dados de um livro."""
    consulta = 'UPDATE livros SET id_autor = ?, titulo_livro = ?, ISBN = ?, ano_publicacao = ?, is_emprestado = ? WHERE id = ?'
    return _executar_query(consulta, (id_autor, titulo_livro, ISBN, ano_publicacao, is_emprestado, id))

def deletar_livro(id):
    """Deleta um livro por ID."""
    return _executar_query('DELETE FROM livros WHERE id = ?', (id,))

# --- Funções CRUD Específicas para Empréstimo (Incluindo Lógica Transacional) ---

def listar_emprestimos():
    """Lista todos os empréstimos com dados de FK para devolução."""
    consulta = """
        SELECT 
            e.id, 
            e.data_emprestimo, 
            e.data_prevista_devolucao, 
            e.data_efetiva_devolucao,
            e.id_cliente, 
            e.id_livro,
            c.nome as nome_cliente,
            l.titulo_livro
        FROM emprestimo e
        JOIN clientes c ON e.id_cliente = c.id
        JOIN livros l ON e.id_livro = l.id
        ORDER BY e.data_emprestimo DESC
    """
    return _executar_query(consulta)

def salvar_emprestimo(id_cliente, id_livro):
    """Inicia o empréstimo e atualiza status do livro e cliente."""
    
    # 1. Registrar o empréstimo 
    consulta_emprestimo = 'INSERT INTO emprestimo (id_cliente, id_livro) VALUES (?, ?)'
    _executar_query(consulta_emprestimo, (id_cliente, id_livro))
    
    # 2. Atualizar o livro: is_emprestado = 1
    consulta_livro = 'UPDATE livros SET is_emprestado = 1 WHERE id = ?'
    _executar_query(consulta_livro, (id_livro,))
    
    # 3. Atualizar o cliente: total_emprestimo + 1
    consulta_cliente = 'UPDATE clientes SET total_emprestimo = total_emprestimo + 1 WHERE id = ?'
    _executar_query(consulta_cliente, (id_cliente,))
    
    return True 

def devolver_livro(id, data_efetiva_devolucao, id_livro, id_cliente):
    """Registra a devolução e atualiza status de livro/cliente."""
    
    # 1. Registrar a data efetiva de devolução
    consulta_emprestimo = 'UPDATE emprestimo SET data_efetiva_devolucao = ? WHERE id = ?'
    _executar_query(consulta_emprestimo, (data_efetiva_devolucao, id))
    
    # 2. Atualizar o livro: is_emprestado = 0
    consulta_livro = 'UPDATE livros SET is_emprestado = 0 WHERE id = ?'
    _executar_query(consulta_livro, (id_livro,))
    
    # 3. Atualizar o cliente: total_emprestimo - 1
    consulta_cliente = 'UPDATE clientes SET total_emprestimo = total_emprestimo - 1 WHERE id = ?'
    _executar_query(consulta_cliente, (id_cliente,))
    
    return True

def buscar_emprestimo_por_id(id):
    """Busca um empréstimo específico por ID."""
    dados = _executar_query('SELECT id, id_cliente, id_livro, data_emprestimo, data_prevista_devolucao, data_efetiva_devolucao FROM emprestimo WHERE id = ?', (id,))
    return dados[0] if dados else None

def deletar_emprestimo(id):
    """Deleta um empréstimo por ID."""
    return _executar_query('DELETE FROM emprestimo WHERE id = ?', (id,))