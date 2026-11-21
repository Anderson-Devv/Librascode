import mysql.connector

def conexao_banco():
    return mysql.connector.connect(
        host ='localhost',
        user ='root',
        password ='91240028Aa.',
        database ='testebancodados',
    )