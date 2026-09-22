import mysql.connector

conexao = mysql.connector.connect(
    host ='localhost',
    user ='root',
    password ='Lga1155.',
    database ='et',
)

cursor = conexao.cursor()

def LeiaInt(msg):
    while True:
        try:
            n = int(input(msg))
        except (ValueError, TypeError):
            print('\033[31mErro: por favor, digite um número válido.\033[m')
            continue
        except (KeyboardInterrupt):
            print('\033[31Usuário não digitou esse número.\033[m')
            return 0
        else:
            return n


def linha(tam=40):
    return '-' * tam

def cabeçalho(txt):
    print(linha())
    print(txt.center(40))
    print(linha())
    
def menu(lista):
    cabeçalho('LIBRASCODE')
    c = 1
    for item in lista:
        print(f'{c} {item}')
        c += 1
    print(linha())
    opc = LeiaInt('Sua opção: ')
    return opc 

while True:
    resposta = menu(['. cadastrar novo usuário', '. logar exibir perfil', '. alterar informações', '. Sair'])    
    if resposta == 1:
        print('cadastrar novo usuário')
    elif resposta == 2:
        print('logar exibir perfil')
    elif resposta == 3:
        print('alterar informações')
    elif resposta == 4:
        print('Saindo do Sistema... Até mais')
        break
    else:
        print('\033[31mErro, opção inválida! Tente novamente.\033[m')

#CRUD

#comando = f'SELECT * FROM cadastrolibrascode'
#cursor.execute(comando)
#conexao.commit() #edita banco de dados
#resultado = cursor.fetchall() # ler banco de dados
#print(resultado)

#CREATE
#usuario = ""
#senha = ""
#comando = f'INSERT INTO cadastrolibrascode (usuario, senha) VALUES ("{usuario}", "{senha}")'
#cursor.execute(comando)
#conexao.commit() # edita banco de dados

#READ
#comando = f'SELECT * FROM cadastrolibrascode'
#cursor.execute(comando)
#resultado = cursor.fetchall() # ler banco de dados
#print(resultado)

#UPDATE
#usuario = ""
#senha = ""
#comando = f'UPDATE cadastrolibrascode SET senha = "{senha}" WHERE usuario = "{usuario}"'
#cursor.execute(comando)
#conexao.commit() #edita banco de dados

#DELETE
#usuario = ""
#comando = f'DELETE FROM cadastrolibrascode WHERE usuario = "{usuario}"'
#cursor.execute(comando)
#conexao.commit() #edita banco de dados

cursor.close()
conexao.close()
