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
    resposta = menu(['. cadastrar novo usuário', '. login', '. Sair', ])    
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
        resultado = fazer_login(email, senha)
        if resultado == True:
            print("Abrindo menu de Login...")
            def menu_login():
                while True:
                    resposta = menu(['. Alterar senha', 'Alterar email', '. Deletar conta', '. Sair'])
                    if resposta == 1:
                        nova_senha = input('Digite a nova senha: \n')
                        cursor.execute(
                            "UPDATE cadastrolibrascode SET senha = %s WHERE email = %s",
                            (nova_senha, email),               
                        )
                        conexao.commit()
                        print("Senha alterada com sucesso.")
                        return menu_login()
                    elif resposta == 2:
                        novo_email = input("Digite novo email: n")
                        cursor.execute(
                        "UPDATE cadastrolibrascode SET email = %s WHERE email = %s",
                        (novo_email, email),
                        )
                        conexao.commit()
                        print("Email alterado com sucesso.")
                        return menu_login()
                    elif resposta == 3:
                        escolha = input("Deseja deletar sua conta S ou N?")
                        if escolha == "S":
                            cursor.execute(
                                "DELETE FROM cadastrolibrascode WHERE email = %s",
                                (email,),
                            )
                            conexao.commit()
                            print("Conta deletada com sucesso")
                            return menu_login()
                        if escolha == "N":
                            print("Deleção cancelada")
                        else:
                            print("Opção inválida\n")
                            return menu_login()
                    elif resposta == 4:
                        print("Voltando ao menu principal")
                        break
                    else:
                        print("Opção inválida, tente uma opção válida da próxima vez.")
                        return
            menu_login()
                        
        if resultado == False:
            print("Você precisa estar logado para acessar o menu de login.")
            break
                            
    elif resposta == 3:
        print('Saindo do Sistema... Até mais')
        break
    else:
        print('\033[31mErro, opção inválida! Tente novamente.\033[m')

cursor.close()
conexao.close()
