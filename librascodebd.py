import mysql.connector

def conexao_banco():
    return mysql.connector.connect(
        host ='localhost',
        user ='root',
        password ='Lga1155.',
        database ='et',
    )