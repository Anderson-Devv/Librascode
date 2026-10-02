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
        print('cadastrar novo usuário: \n')
        usuario = input("Digite o nome do novo usuário: \n")
        senha = input("Digite a nova senha: \n")
        while len(senha) < 8:
            print('Senha precisa ter pelo menos 8 caracteres.')
            senha = input("Digite a nova senha: \n")

        cursor.execute(
            "INSERT INTO cadastrolibrascode (usuario, senha) VALUES (%s, %s)",
            (usuario, senha),
        )
        conexao.commit()
        print('Usuário cadastrado com sucesso')
    elif resposta == 2:
        for tentativa in range(3):
            login = input("Digite seu login para ver se está cadastrado: ")
            cursor.execute(
                "SELECT usuario FROM cadastrolibrascode WHERE usuario = %s",
                (login,),
            )
            resultado = cursor.fetchone()

            if resultado:
                print(f"Usuário cadastrado: {resultado[0]}")
                break

            print(f"Erro {tentativa + 1}/3: usuário não encontrado.")
            if tentativa == 2:
                print("Limite de tentativas atingido. Voltando ao menu principal.")
    elif resposta == 3:
        for tentativa1 in range(3):
                    usuario = input("Digite o usuário que deseja deletar: ")
                    cursor.execute(
                        "SELECT 1 FROM cadastrolibrascode WHERE usuario = %s",
                        (usuario,),
                    )
                    resultado = cursor.fetchone()
        
                    if resultado:
                        cursor.execute(
                            "DELETE FROM cadastrolibrascode WHERE usuario = %s",
                            (usuario,),
                        )
                        conexao.commit()
                        print('Usuário deletado com sucesso')
                        break
        
                    print(f"Erro {tentativa1 + 1}/3: usuário não encontrado.")
                    if tentativa1 == 2:
                        print("Limite de tentativas atingido. Voltando ao menu principal.")
                        
    elif resposta == 4:
        print('Saindo do Sistema... Até mais')
        break
    else:
        print('\033[31mErro, opção inválida! Tente novamente.\033[m')

cursor.close()
conexao.close()
