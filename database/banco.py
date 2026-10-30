
# Importando as bibliotecas
import sqlite3
import os


# Definindo onde o banco vai ficar salvo
CAMINHO_BANCO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "atletas.db"
)


# Criando a conexao com o banco
def conectar():

    conexao = sqlite3.connect(CAMINHO_BANCO)

    return conexao


# Criando a tabela dos atletas
def criar_tabela():

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS atletas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data_nascimento TEXT,
            sexo TEXT,
            modalidade TEXT,
            equipe TEXT,
            posicao TEXT,
            telefone TEXT,
            email TEXT
        )
    """)

    conexao.commit()
    conexao.close()


# Cadastrando um atleta no banco
def cadastrar_atleta(nome, data_nascimento, sexo, modalidade,
                     equipe, posicao, telefone, email):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO atletas (
            nome, data_nascimento, sexo, modalidade,
            equipe, posicao, telefone, email
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        nome, data_nascimento, sexo, modalidade,
        equipe, posicao, telefone, email
    ))

    conexao.commit()
    conexao.close()


# Buscando todos os atletas cadastrados
def listar_atletas():

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM atletas ORDER BY nome")

    atletas = cursor.fetchall()

    conexao.close()

    return atletas


# Buscando um atleta pelo ID
def buscar_atleta(id_atleta):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM atletas WHERE id = ?",
        (id_atleta,)
    )

    atleta = cursor.fetchone()

    conexao.close()

    return atleta


# Alterando os dados de um atleta
def editar_atleta(id_atleta, nome, data_nascimento, sexo,
                  modalidade, equipe, posicao, telefone, email):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE atletas
        SET nome = ?,
            data_nascimento = ?,
            sexo = ?,
            modalidade = ?,
            equipe = ?,
            posicao = ?,
            telefone = ?,
            email = ?
        WHERE id = ?
    """, (
        nome, data_nascimento, sexo, modalidade,
        equipe, posicao, telefone, email, id_atleta
    ))

    conexao.commit()
    conexao.close()


# Excluindo um atleta pelo ID
def excluir_atleta(id_atleta):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM atletas WHERE id = ?",
        (id_atleta,)
    )

    conexao.commit()
    conexao.close()


# Contando quantos atletas estao cadastrados
def contar_atletas():

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) FROM atletas")

    total = cursor.fetchone()[0]

    conexao.close()

    return total