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
            print("\nLogin realizado com sucesso! Bem-vindo.\n")
            return True
        else:
            print("\nUsuário ou senha incorretos.\n")
            return False
        
    except mysql.connector.Error as erro:
        print(f"Erro no login: {erro}")
        
    finally:
        if cursor is not None:
            cursor.close()
        elif conexao is not None:
            conexao.close() 