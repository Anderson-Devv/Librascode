import mysql.connector

def conexao_banco():
    return mysql.connector.connect(
        host ='localhost',
        user ='root',
<<<<<<< HEAD
        password ='91240028Aa.',
        database ='testebancodados',
=======
        password ='Lga1155.',
        database ='et',
>>>>>>> 78c1244f7fdad7e26d30310623d4f703d452597a
    )