import pymysql
from pymysql.cursors import DictCursor

def conectar_ao_banco():
    try:
        conexao = pymysql.connect(
            host='localhost',
            user='root',
            password='16112004',  # substitua pela sua senha real
            database='ph_agua',
            cursorclass=DictCursor
        )
        return conexao
    except pymysql.MySQLError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise
