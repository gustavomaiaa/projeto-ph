import pymysql

try:
    conexao = pymysql.connect(
        host="localhost",
        user="root",
        password="16112004",
        database="ph_agua"
    )
    print("Conectado com sucesso ao banco de dados!")
    conexao.close()
except Exception as e:
    print("Erro ao conectar ao banco:", e)
