import mysql.connector

from librascodebd import conexao_banco

def fazer_login(email, senha):
    conexao = None
    cursor = None
    try:
        conexao = conexao_banco()
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT * FROM cadastrolibrascode WHERE email = %s AND senha = %s",
            (email, senha),
        )
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
        if cursor is not None:
            cursor.close()
        if conexao is not None:
            conexao.close() 