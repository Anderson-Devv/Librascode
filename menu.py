from librascodebd import conexao_banco
from time import sleep
import os
from login import fazer_login
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
            print('\033[31 Usuário não digitou esse número.\033[m')
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
    resposta = menu(['. cadastrar novo usuário', '. login', '. deletar usuario', '. sair' ])    
    if resposta == 1:
        print('cadastrar novo usuário: \n')
        while True:
            email = input("Digite seu email(apenas institucional): \n")
            cursor.execute(
                "SELECT email FROM librascode WHERE email = %s LIMIT 1",
                (email,)
            )
            resultado = cursor.fetchone() 
            if "@ufrpe.br" not in email:
                print('email inválido, digite um email válido (com @ufrpe.br)')
                sleep(2)
                os.system('cls' if os.name == 'nt' else 'clear')
            elif resultado is not None:
                print("Este email ja esta cadastrado!!")
                sleep(2)
                os.system('cls' if os.name == 'nt' else 'clear')

            else:
                break
        while True:
            senha = input("Digite a nova senha(min 8 caracteres/max 15 caracteres): \n") 
            if len(senha) < 8:
                print('senha precisa ter pelo menos 8 caracteres, digite novamente')
                sleep(2)
                os.system('cls' if os.name == 'nt' else 'clear')
            elif len(senha) > 15:
                print('A senha ultrapassar os 15 caracteres')
            else:
                break
        while True:
                usuario = input("Digite o nome do novo usuário(max 15 caracteres): \n")
                cursor.execute(
                     "SELECT usuario FROM librascode WHERE usuario = %s LIMIT 1",
                     (usuario,)
                )
                resultado = cursor.fetchone()
                if resultado is not None:
                    print("Esse nome de usuário ja existe!!")
                    sleep(2)
                    os.system('cls' if os.name == 'nt' else 'clear')

                elif len(usuario) < 3:
                    print('nome de usuario menor que 3 caracteres, tente novamente')
                    sleep(2)
                    os.system('cls' if os.name == 'nt' else 'clear')
                elif len(usuario) > 15:
                    print('nome de usuario maior que 15 caracteres, tente novamente')                     
                    sleep(2)
                    os.system('cls' if os.name == 'nt' else 'clear')
                else:
                    comando = f'INSERT INTO librascode (usuario, senha, email) VALUES ("{usuario}", "{senha}", "{email}")'
                    print('Usuário cadastrado com sucesso')
                    cursor.execute(comando)
                    conexao.commit()
                    sleep(2)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
    elif resposta == 2:
        while True:
            fazer_login()
            if resposta == 1:
                for tentativa1 in range(3):
                    usuario = input("Digite o usuário que deseja alterar as informações: ")
                    cursor.execute(
                        "SELECT 1 FROM librascode WHERE usuario = %s",
                        (usuario,),
                    )
                    resultado = cursor.fetchone()

                    if resultado is not None:
                        print('O que você deseja alterar?')
                        alterar = menu(['. Nome de usuário', '. Email', '. Senha'])
                

    elif resposta == 3:
        for tentativa in range(3):
            email_usuario = input("Digite o email do usuário que deseja deletar: \n")
            senha_usuario = input("Digite a senha para confirmar exclusão: \n")
            cursor.execute(
            "SELECT 1 FROM librascode WHERE email = %s and senha = %s",
                (email_usuario, senha_usuario,),
            )
            resultado = cursor.fetchone()
    
            if resultado:
                cursor.execute(
                    "DELETE FROM librascode WHERE email = %s and senha = %s",
                    (email_usuario, senha_usuario,),
                )
                conexao.commit()
                print('Usuário deletado com sucesso')
                break
        
            print(f"Erro {tentativa + 1}/3: usuário não encontrado.")
            if tentativa == 2:
                print("Limite de tentativas atingido. Voltando ao menu principal.")
                        
    elif resposta == 4:
        print('Saindo do Sistema... Até mais')
        sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        break

    else:
        print('\033[31mErro, opção inválida! Tente novamente.\033[m')

cursor.close()
conexao.close()
