import mysql.connector
from tkinter import messagebox
import customtkinter as ctk

from gerenciamento_dados.librascodebd import conexao_banco

class Conta:
    
    def __init__(self, email, usuario, senha):
        self.email = email
        self.usuario = usuario
        self.senha = senha
        

    def fazer_login(self):
        conexao = None
        cursor = None
        try:
            conexao = conexao_banco()
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT idlibrascode FROM librascode WHERE email = %s AND senha = %s",
                (self.email, self.senha),
            )
            resultado = cursor.fetchone()
            
            if resultado:
                print("\nLogin realizado com sucesso! Bem-vindo.\n")
                return resultado[0]
            else:
                print("\nUsuário ou senha incorretos.\n")
                return 
            
        except mysql.connector.Error as erro:
            print(f"Erro no login: {erro}")
            
        finally:
            if cursor is not None:
                cursor.close()
            if conexao is not None:
                conexao.close()

    def cadastrar(self):

        conexao = None
        cursor = None

        try:
            conexao = conexao_banco()
            cursor = conexao.cursor()

            cursor.execute(
                "SELECT idlibrascode FROM librascode WHERE email = %s",
                (self.email,)
            )

            resultado = cursor.fetchone()

            if resultado:
                return "email_existente"

            if len(self.usuario) < 3 or len(self.usuario) > 15:
                return "usuario_invalido"

            if not self.email.endswith("@ufrpe.br"):
                return "email_invalido"

            if len(self.senha) < 8 or len(self.senha) > 15:
                return "senha_invalida"

            cursor.execute(
                """
                INSERT INTO librascode
                (usuario, senha, email)
                VALUES (%s, %s, %s)
                """,
                (self.usuario, self.senha, self.email)
            )

            conexao.commit()

            return True

        except mysql.connector.Error as erro:
            print(f"Erro ao cadastrar: {erro}")
            return False

        finally:
            if cursor:
                cursor.close()

            if conexao:
                conexao.close()

    def alterar_senha(self):

        dialog = ctk.CTkInputDialog(
            text="Digite a nova senha",
            title="Alterar senha"
        )

        nova_senha = dialog.get_input()

        if not nova_senha:
            return False

        if self.senha == nova_senha:
            return "senha_usada"

        if len(nova_senha) < 8 or len(nova_senha) > 15:
            return "senha_invalida"

        conf_senha = ctk.CTkInputDialog(
            text="Confirme sua senha",
            title="Confirmação de senha"
        )

        confirmar_senha = conf_senha.get_input()

        if not confirmar_senha:
            return False

        if nova_senha != confirmar_senha:
            return "senhas_diferentes"

        conexao = None
        cursor = None

        try:
            conexao = conexao_banco()
            cursor = conexao.cursor()


            cursor.execute(
                """
                UPDATE librascode
                SET senha=%s
                WHERE email=%s
                """,
                (nova_senha, self.email)
            )

            conexao.commit()

            self.senha = nova_senha

            return True
        
        except mysql.connector.Error as erro:
            print(f"conexão com o banco falhou{erro}")
            return False

        finally:
            if cursor is not None:
                cursor.close()
            if conexao is not None:
                conexao.close()



    def alterar_email(self):

        dialog = ctk.CTkInputDialog(
            text="Digite o novo email",
            title="Alterar email"
        )

        novo_email = dialog.get_input()

        if not novo_email:
            return False

        if not novo_email.endswith("@ufrpe.br"):
            return "email_invalido"

        if novo_email == self.email:
            return "email_igual"

        conexao = None
        cursor = None

        try:
            conexao = conexao_banco()
            cursor = conexao.cursor()

            cursor.execute(
                """
                UPDATE librascode
                SET email=%s
                WHERE email=%s
                """,
                (novo_email, self.email)
            )

            conexao.commit()

            self.email = novo_email

            return True

        except mysql.connector.Error as erro:
            print(f"erro ao conectar banco{erro}")

        finally:
            if cursor is not None:
                cursor.close()
            if conexao is not None:
                conexao.close()


    def deletar_conta(self):

        resposta = messagebox.askyesno(
            "Confirmação",
            "Deseja realmente deletar sua conta?"
        )

        if resposta:

            conexao = None
            cursor = None

            try:
                conexao = conexao_banco()
                cursor = conexao.cursor()

                cursor.execute(
                    """
                    DELETE FROM librascode
                    WHERE email=%s
                    """,
                    (self.email,)
                )

                conexao.commit()

                messagebox.showinfo(
                    "Sucesso",
                    "Conta deletada!"
                )
                return True
            
            except mysql.connector.Error as erro:
                print(f'erro ao conectar banco{erro}')

            finally:
                if cursor is not None:
                    cursor.close()
                if conexao is not None:
                    conexao.close()
