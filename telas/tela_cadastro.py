
import customtkinter as ctk

from conta.gerenciamento_conta import Conta
from tkinter import messagebox


class TelaCadastro(ctk.CTkFrame):

    def __init__(self, master, controlador):
        super().__init__(master)

        self.controlador = controlador

        self.criar_componentes()

    def criar_componentes(self):

        self.label_mensagem = ctk.CTkLabel(
        self,
        text="",
        text_color="red"
        )


        ctk.CTkLabel(
            self,
            text="Cadastro",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        ctk.CTkLabel(
            self,
            text="Nome de Usuário"
        ).pack(pady=10)

        self.campo_usuario = ctk.CTkEntry(
            self,
            width=300
        )
        self.campo_usuario.pack()

        ctk.CTkLabel(
            self,
            text="Email"
        ).pack(pady=10)

        self.campo_email = ctk.CTkEntry(
            self,
            width=300
        )
        self.campo_email.pack()

        ctk.CTkLabel(
            self,
            text="Senha"
        ).pack(pady=10)

        self.campo_senha = ctk.CTkEntry(
            self,
            width=300,
            show="*"
        )
        self.campo_senha.pack()

        ctk.CTkLabel(
            self,
            text="Confirmação de Senha"
        ).pack(pady = 10)


        self.campo_conf_senha = ctk.CTkEntry(
            self,
            width=300,
            show="*"
        )
        self.campo_conf_senha.pack()

        ctk.CTkButton(
            self,
            text="Cadastrar",
            width=200,
            command=self.cadastrar
        ).pack(pady=20)

        ctk.CTkButton(
            self,
            text="Voltar ao Login",
            command=lambda: self.controlador.mostrar_tela("login")
        ).pack(pady=10)

    def cadastrar(self):

        usuario = self.campo_usuario.get()
        email = self.campo_email.get()
        senha = self.campo_senha.get()
        confirmar_senha = self.campo_conf_senha.get()

        if senha != confirmar_senha:
            self.label_mensagem.configure(
            text="As senhas não coincidem!",
            text_color="red"
            )
            self.label_mensagem.pack(pady = 5)
            return

        conta = Conta(email, usuario, senha)

        resultado = conta.cadastrar()

        if resultado:
            self.controlador.mostrar_tela("login")