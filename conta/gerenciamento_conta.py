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
                """
                SELECT idcadastrolibrascode, usuario
                FROM cadastrolibrascode
                WHERE email = %s AND senha = %s
                """,
                (self.email, self.senha)
            )
            resultado = cursor.fetchone()
            
            if resultado:
                self.usuario = resultado[1]
                
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
                "SELECT idcadastrolibrascode FROM cadastrolibrascode WHERE email = %s",
                (self.email,)
            )
        
            resultado = cursor.fetchone()
        
            if len(self.usuario) < 3 or len(self.usuario) > 15:
                messagebox.showerror("Erro","Usuário deve ter entre 3 e 15 caracteres.")
                return 

            if "@ufrpe.br" not in self.email:
                messagebox.showerror("Erro", "Email precisa conter @ufrpe.br")
                return 

            if len(self.senha) < 8 or len(self.senha) > 15:
                messagebox.showerror("Erro", "Senha deve ter entre 8 e 15 caracteres.")
                return

            if resultado:
                return "email_existente"

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
        
        if self.senha == nova_senha:
            messagebox.showerror("Erro", "A senha já está sendo usada, tente uma senha diferente.")
            return
        
        conf_senha = ctk.CTkInputDialog(
            text="Confirme sua senha",
            title="Confirmação de senha"
        )

        confirmar_senha = conf_senha.get_input()

        if not confirmar_senha:
            return False

        if nova_senha != confirmar_senha:
            return "senhas_diferentes"
        
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
        
        if novo_email == self.email:
            messagebox.showerror("Erro", "Email igual ao anterior, tente um email novo.")
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
                    DELETE FROM usuario_conquistas
                    WHERE usuario_id =
                    (
                        SELECT idcadastrolibrascode
                        FROM cadastrolibrascode
                        WHERE email = %s
                    )
                    """,
                    (self.email,)
                )
                
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

    def alterar_usuario(self):
        
        dialog = ctk.CTkInputDialog(
            text="Digite o novo usuário",
            title="Alterar usuário"
        )
        
        novo_usuario = dialog.get_input()
        
        if not novo_usuario:
            return False
        
        if len(novo_usuario) < 3 or len(novo_usuario) > 15:
            messagebox.showerror("Erro", "Nome de usuário inválido, tente um nome com mais de 3 caracteres e menos de 15")
            return
        
        if novo_usuario == self.usuario:
            messagebox.showerror("Erro", "Nome de usuário inválido, tente um nome diferente")
            return
        
        try:
            self._executar(
                """
                UPDATE cadastrolibrascode
                SET usuario = %s
                WHERE email = %s
                """,
                (novo_usuario, self.email)
            )
            
            self.usuario = novo_usuario
            
        except Exception as erro:
                messagebox.showerror("Erro", str(erro))
                return
        
        messagebox.showinfo("Sucesso", "Novo nome de Usuário alterado com sucesso!")
        return True