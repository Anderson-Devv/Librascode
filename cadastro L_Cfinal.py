import mysql.connector
from librascodebd import conexao_banco

conexao = conexao_banco()
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
    opçoes = 1
    for item in lista:
        print(f'{opçoes} {item}')
        opçoes += 1
    print(linha())
    opc = LeiaInt('Sua opção: ')
    return opc 

while True:
    resposta = menu(['. cadastrar novo usuário', '. exibir perfil', '. deletar usuário', '. login', '. Sair', ])    
    if resposta == 1:
        print('cadastrar novo usuário: \n')
        email = input("Digite seu email: \n")
        while True: 
            if "@ufrpe.br" not in email:
                print('email inválido, digite um email válido (com @ufrpe.br)')
                break
            senha = input("Digite a nova senha: \n")
            while True: 
                if len(senha) < 8:
                    print('senha precisa ter pelo menos 8 caracteres')
                    break
                else:
                    usuario = input("Digite o nome do novo usuário: \n")
                    comando = f'INSERT INTO cadastrolibrascode (usuario, senha, email) VALUES ("{usuario}", "{senha}", "{email}")'
                    print('Usuário cadastrado com sucesso')
                    cursor.execute(comando)
                    conexao.commit()
                    break
    elif resposta == 2:
        for tentativa in range(3):
            login = input("Digite seu login (seu email) para ver se está cadastrado: ")
            cursor.execute(
                "SELECT usuario FROM cadastrolibrascode WHERE email = %s",
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
                    email_usuario = input("Digite o email do usuário que deseja deletar: \n")
                    senha_usuario = input("Digite a senha para confirmar exclusão: \n")
                    cursor.execute(
                        "SELECT 1 FROM cadastrolibrascode WHERE email = %s and senha = %s",
                        (email_usuario, senha_usuario,),
                    )
                    resultado = cursor.fetchone()
        
                    if resultado:
                        cursor.execute(
                            "DELETE FROM cadastrolibrascode WHERE email = %s and senha = %s",
                            (email_usuario, senha_usuario,),
                        )
                        conexao.commit()
                        print('Usuário deletado com sucesso')
                        break
        
                    print(f"Erro {tentativa1 + 1}/3: usuário não encontrado.")
                    if tentativa1 == 2:
                        print("Limite de tentativas atingido. Voltando ao menu principal.")
    elif resposta == 4:
        def fazer_login(email, senha):
            try:
                conexao = conexao_banco()
                cursor = conexao.cursor()
                login = "SELECT * FROM cadastrolibrascode WHERE email = %s AND senha = %s"
                cursor.execute(login, (email, senha))
                resultado = cursor.fetchone()
        
                if resultado:
                    print("Login realizado com sucesso! Bem-vindo.")
                    return True
                else:
                    print("Usuário ou senha incorretos.")
                    return False
            except mysql.connector.Error as erro:
                print(f"Erro no login: {erro}")
            finally:
                if conexao.is_connected():
                    cursor.close()
                    conexao.close()
 
                            
    elif resposta == 5:
        print('Saindo do Sistema... Até mais')
        break
    else:
        print('\033[31mErro, opção inválida! Tente novamente.\033[m')

cursor.close()
conexao.close()
