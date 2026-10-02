from librascodebd import conexao_banco

conexao = conexao_banco()

print(conexao)

cursor = conexao.cursor()
#CRUD

# comando = f'SELECT * FROM testebancodados'

# usuario = (input('digite o nome do novo usuário'))
# senha = (input('digite a sua senha'))
# comando = f'INSERT INTO librascode (usuario, senha) VALUES (  %s, %s )'
# VALUES = (usuario, senha)
# cursor.execute(comando, VALUES)
# conexao.commit() #edita banco de dados


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
