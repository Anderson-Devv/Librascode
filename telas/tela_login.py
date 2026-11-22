
import customtkinter as ctk
from tkinter import messagebox

from conta.gerenciamento_conta import Conta


class TelaLogin(ctk.CTkFrame):

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

        self.label_mensagem.pack(pady=10)

        ctk.CTkLabel(
            self,
            text="Login",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

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

        ctk.CTkButton(
            self,
            text="Entrar",
            command=self.logar
        ).pack(pady=20)

        ctk.CTkButton(
            self,
            text="Criar conta",
            command=lambda: self.controlador.mostrar_tela("cadastro")
        ).pack(pady=10)

    def logar(self):
        email = self.campo_email.get()
        senha = self.campo_senha.get()

        self.conta = Conta(email, "", senha)

        resultado = self.conta.fazer_login()

        if resultado:

            menu = self.controlador.telas["menu"]
            menu.configurar_usuario(email, resultado, self.conta)

            self.controlador.mostrar_tela("menu")

        else:
            self.label_mensagem.configure(
                text="email ou senha incorretos!!",
                text_color="red"
            )
            self.label_mensagem.pack(pady = 5)

