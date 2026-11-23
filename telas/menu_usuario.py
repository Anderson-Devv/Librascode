import customtkinter as ctk
from conta.gerenciamento_conta import Conta
from telas.fundo import FundoEscalavel

class MenuUsuario(ctk.CTkFrame):

    def __init__(self, master, controlador):

        super().__init__(master)

        self.controlador = controlador

        self.fundo = FundoEscalavel(self, "500x400.jpeg")

        self.email = None
        self.usuario_id = None
        self.criar_componentes()

    def criar_componentes(self):

        self.label_usuario = ctk.CTkLabel(
            self,
            text="Usuário não identificado",
            font=("Arial", 20)
        )

        self.label_usuario.pack(pady=20)

        ctk.CTkButton(
            self,
            text="Abrir lição",
            width=250,
            command=self.fazer_licao
         ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Alterar Senha",
            width=250,
            command=self.alterar_senha
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Alterar Email",
            width=250,
            command=self.alterar_email
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Deletar Conta",
            width=250,
            fg_color="red",
            hover_color="#990000",
            command=self.deletar_conta
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Sair",
            width=250,
            command=lambda: self.controlador.mostrar_tela("login")
        ).pack(pady=10)

        ctk.CTkButton(
             self,
             text="Ranking",
             width=250,
             command=self.abrir_ranking
         ).pack(pady=10)

    def fazer_licao(self):

        modulos = self.controlador.telas["modulos"]
        modulos.configurar_usuario(self.usuario_id)
        self.controlador.mostrar_tela("modulos")

    def abrir_ranking(self):
        
        ranking = self.controlador.telas["ranking"]
        ranking.configurar_usuario(self.usuario_id)
        self.controlador.mostrar_tela("ranking")

    def alterar_senha(self):

        self.conta.alterar_senha()

    def alterar_email(self):

        if self.conta.alterar_email():
            self.email = self.conta.email
            self.label_usuario.configure(
                text=f"Usuário logado:\n{self.email}"
            )

    def deletar_conta(self):

        if self.conta.deletar_conta():
            self.controlador.mostrar_tela("login")
        
    def configurar_usuario(self, email, usuario_id, conta):
        self.email = email
        self.usuario_id = usuario_id
        self.conta = conta

        self.label_usuario.configure(
            text=f"Usuário logado:\n{self.email}"
        )