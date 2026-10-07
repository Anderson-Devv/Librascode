from librascodebd import conexao_banco
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
    resposta = menu(['. cadastrar novo usuário', '. login', '. deletar usuário', '. Sair', ])    
    if resposta == 1:
        print('cadastrar novo usuário: \n')

        while True:
            email = input("Digite seu email: \n") 
            if "@ufrpe.br" not in email:
                print('email inválido, digite um email válido (com @ufrpe.br)')
            else:
                break
        while True:
            senha = input("Digite a nova senha: \n")
            if len(senha) < 8 or len(senha) > 15:
                print('senha precisa ter pelo menos 8 caracteres e menos de 15 caracteres')
            else:
                break
        while True:
                usuario = input("Digite o nome do novo usuário: (mínimo de 3 caracteres e máximo de 15)\n")
                if len(usuario) < 3 or len(usuario) >15:
                    print('Nome de usuário inválido, o nome deve ter pelo mens 3 caracteres e nó máximo 15.')
                else:
                    comando = f'INSERT INTO cadastrolibrascode (usuario, senha, email) VALUES ("{usuario}", "{senha}", "{email}")'
                    print('Usuário cadastrado com sucesso')
                    cursor.execute(comando)
                    conexao.commit()
                    break
    elif resposta == 2:
        email = input("Digite seu email: \n")
        senha = input("Digite sua senha: \n")
        fazer_login(email, senha)
        
    elif resposta == 3:
        for tentativa in range(3):
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
        print('Saindo do Sistema... Até mais')
        break
    else:
        print('\033[31mErro, opção inválida! Tente novamente.\033[m')

cursor.close()
conexao.close()
