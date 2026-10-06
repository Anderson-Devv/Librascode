from librascodebd import conexao_banco

def fazer_login():
    try:
        conexao = conexao_banco()
        cursor = conexao.cursor()
        email = input("digite seu email: ")
        senha = input("digite sua senha: ")
        login = "SELECT * FROM librascode WHERE email = %s AND senha = %s"
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
fazer_login()