import sqlite3
from pathlib import Path
# path é utilizado para localizar series.json
BASE_DIR = Path(__file__).resolve().parent.parent
# Encomtra a raiz do projeto
DATABASE_FILE = BASE_DIR / 'series.db'
# define onde o banco ficará


def conectar():
    return sqlite3.connect(DATABASE_FILE)

def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS series (
            titulo TEXT PRIMARY KEY,
            genero TEXT,
            ano_lancamento INTEGER,
            temporadas INTEGER
        )
    """)

    conexao.commit()
    conexao.close()

def buscar_por_titulo(titulo):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT titulo, genero, ano_lancamento, temporadas
        FROM series
        WHERE LOWER(titulo) = LOWER(?)
        """,
        (titulo,)
    )

    serie = cursor.fetchone()

    conexao.close()

    return serie
