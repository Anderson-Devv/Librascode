from librascodebd import conexao_banco
from time import sleep
import os

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
    resposta = menu(['. cadastrar novo usuário', '. exibir perfil', '. alterar informações', '. Sair'])    
    if resposta == 1:
        print('cadastrar novo usuário: \n')
        email = input("Digite seu email: \n")
        while True: 
                if "@ufrpe.br" not in email:
                    print('email inválido, digite um email válido (com @ufrpe.br)')
                    os.system('cls' if os.name == 'nt' else 'clear')

                else:
                    break
        senha = input("Digite a nova senha: \n")
        while True: 
            if len(senha) < 8:
                print('senha precisa ter pelo menos 8 caracteres, digite novamente')
                sleep(2)
                os.system('cls' if os.name == 'nt' else 'clear')

            
            else:
                usuario = input("Digite o nome do novo usuário: \n")
                comando = f'INSERT INTO librascode (usuario, senha, email) VALUES ("{usuario}", "{senha}", "{email}")'
                print('Usuário cadastrado com sucesso')
                cursor.execute(comando)
                conexao.commit()
                sleep(2)
                os.system('cls' if os.name == 'nt' else 'clear')
                break

    elif resposta == 2:
        for tentativa in range(3):
            login = input("Digite seu login (seu email) para ver se está cadastrado: ")
            cursor.execute(
                "SELECT usuario FROM librascode WHERE email = %s",
                (login,),
            )
            resultado = cursor.fetchone()
            sleep(2)
            os.system('cls' if os.name == 'nt' else 'clear')

            if resultado:
                print(f"Usuário cadastrado: {resultado[0]} ")
                sleep(2)
                os.system('cls' if os.name == 'nt' else 'clear')
                break

            print(f"Erro {tentativa + 1}/3: usuário não encontrado.")
            if tentativa == 2:
                print("Limite de tentativas atingido. Voltando ao menu principal.")
                sleep(2)
                os.system('cls' if os.name == 'nt' else 'clear')
    elif resposta == 3:
        for tentativa1 in range(3):
                    usuario = input("Digite o usuário que deseja deletar: ")
                    cursor.execute(
                        "SELECT 1 FROM librascode WHERE usuario = %s",
                        (usuario,),
                    )
                    resultado = cursor.fetchone()
        
                    if resultado:
                        cursor.execute(
                            "DELETE FROM librascode WHERE usuario = %s",
                            (usuario,),
                        )
                        conexao.commit()
                        print('Usuário deletado com sucesso')
                        sleep(1)
                        os.system('cls' if os.name == 'nt' else 'clear')
                        break
        
                    print(f"Erro {tentativa1 + 1}/3: usuário não encontrado.")
                    if tentativa1 == 2:
                        print("Limite de tentativas atingido. Voltando ao menu principal.")
                        sleep(2)
                        os.system('cls' if os.name == 'nt' else 'clear')
                        
    elif resposta == 4:
        print('Saindo do Sistema... Até mais')
        sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        break
    else:
        print('\033[31mErro, opção inválida! Tente novamente.\033[m')

cursor.close()
conexao.close()
