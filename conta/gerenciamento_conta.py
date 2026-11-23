import mysql.connector
from tkinter import messagebox
import customtkinter as ctk
from gerenciamento_dados.librascodebd import conexao_banco

class Conta:
    
    def __init__(self, email, usuario, senha):
        self.email = email
        self.usuario = usuario
        self.senha = senha

    def _executar(self, sql, params):
        conexao = conexao_banco()
        try:
            cursor = conexao.cursor()
            cursor.execute(sql, params)
            conexao.commit()
            cursor.close()
        finally:
            conexao.close()

    def fazer_login(self):
        conexao = None
        cursor = None
        try:
            conexao = conexao_banco()
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT idcadastrolibrascode FROM cadastrolibrascode WHERE email = %s AND senha = %s",
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

        if len(self.usuario) < 3 or len(self.usuario) > 15:
            messagebox.showerror("Erro","Usuário deve ter entre 3 e 15 caracteres.")
            return 

        if "@ufrpe.br" not in self.email:
            messagebox.showerror("Erro", "Email precisa conter @ufrpe.br")
            return 

        if len(self.senha) < 8 or len(self.senha) > 15:
            messagebox.showerror("Erro", "Senha deve ter entre 8 e 15 caracteres.")
            return 

        try:

            self._executar(
                """
                INSERT INTO cadastrolibrascode
                (usuario, senha, email)
                VALUES (%s,%s,%s)
                """,
                (self.usuario, self.senha, self.email)
            )
        except Exception as erro:
            messagebox.showerror("Erro", str(erro))
            return False

        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        return True

    def alterar_senha(self):

        dialog = ctk.CTkInputDialog(
            text="Digite a nova senha",
            title="Alterar senha"
        )

        nova_senha = dialog.get_input()

        if not nova_senha:
            return
        
        if len(nova_senha) < 8 or len(nova_senha) > 15:
            messagebox.showerror("Erro", "Senha deve ter entre 8 e 15 caracteres.")
            return

        try:
            self._executar(
                """
                UPDATE cadastrolibrascode
                SET senha=%s
                WHERE email=%s
                """,
            (nova_senha, self.email)
        )
        except Exception as erro:
            messagebox.showerror("Erro", str(erro))
            return

        self.senha = nova_senha
        messagebox.showinfo("Sucesso", "Senha alterada!")
        return True


    def alterar_email(self):

        dialog = ctk.CTkInputDialog(
            text="Digite o novo email",
            title="Alterar email"
        )
        novo_email = dialog.get_input()
        
        if not novo_email:
            return
        
        if "@ufrpe.br" not in novo_email:
            messagebox.showerror("Erro", "Email precisa conter @ufrpe.br")
            return
                        
        try:
            self._executar(
            """
                UPDATE cadastrolibrascode
                SET email=%s
                WHERE email=%s
                """,
                (novo_email, self.email)
        )
        except Exception as erro:
            messagebox.showerror("Erro", str(erro))
            return
        
        self.email = novo_email
        messagebox.showinfo("Sucesso", "Email alterado!")
        return True

    def deletar_conta(self):

        resposta = messagebox.askyesno(
            "Confirmação",
            "Deseja realmente deletar sua conta?"
        )

        if resposta:

            try:
                self._executar(
                    """
                    DELETE FROM cadastrolibrascode
                    WHERE email=%s
                    """,
                    (self.email,),
            )
            except Exception as erro:
                messagebox.showerror("Erro", str(erro))
                return

            messagebox.showinfo("Sucesso", "Conta deletada!")
            return True
