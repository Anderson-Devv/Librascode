import mysql.connector

conexao = mysql.connector.connect(
    host ='localhost',
    user ='root',
    password ='Lga1155.',
    database ='et',
)

cursor = conexao.cursor()

#CRUD

comando = f'SELECT * FROM cadastrolibrascode'
cursor.execute(comando)
#conexao.commit() edita banco de dados
resultado = cursor.fetchall() # ler banco de dados
print(resultado)

#CREATE
#usuario = "enzo"
#senha = "ryzen5500"
#comando = f'INSERT INTO cadastrolibrascode (usuario, senha) VALUES ("{usuario}", "{senha}")'
#cursor.execute(comando)
#conexao.commit() # edita banco de dados

#READ
#comando = f'SELECT * FROM cadastrolibrascode'
#cursor.execute(comando)
#resultado = cursor.fetchall() # ler banco de dados
#print(resultado)

#UPDATE
#usuario = "enzo"
#senha = "ryzen1"
#comando = f'UPDATE cadastrolibrascode SET senha = "{senha}" WHERE usuario = "{usuario}"'
#cursor.execute(comando)
#conexao.commit() #edita banco de dados

#DELETE
#usuario = "enzo"
#comando = f'DELETE FROM cadastrolibrascode WHERE usuario = "{usuario}"'
#cursor.execute(comando)
#conexao.commit() #edita banco de dados

cursor.close()
conexao.close()
