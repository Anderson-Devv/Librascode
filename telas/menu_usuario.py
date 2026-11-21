
import customtkinter as ctk

from conta.gerenciamento_conta import Conta
# from telas.Licoes.modulo import TelaModulos
# from telas.Licoes.ranking import TelaRanking


class MenuUsuario(ctk.CTkFrame):

    def __init__(self, master, controlador):

        super().__init__(master)

        self.controlador = controlador

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
            command=lambda: self.conta.alterar_senha()
            ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Alterar Email",
            width=250,
            command=lambda: self.conta.alterar_email()
            ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Deletar Conta",
            width=250,
            fg_color="red",
            hover_color="#990000",
            command=lambda: self.conta.deletar_conta()
            ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Sair",
            width=250,
            command=lambda: self.controlador.mostrar_tela("login")
        ).pack(pady=10)

        # ctk.CTkButton(
        #     self,
        #     text="Ranking",
        #     width=250,
        #     command=self.abrir_ranking
        # ).pack(pady=10)

    def fazer_licao(self):

        tela = self.controlador.telas["modulos"]

        tela.configurar_usuario(self.usuario_id)

        self.controlador.mostrar_tela("modulos")
    # def abrir_ranking(self):

    #     TelaRanking(
    #         self,
    #         self.usuario_id
    #     )

    def configurar_usuario(self, email, usuario_id, conta):
        self.email = email
        self.usuario_id = usuario_id
        self.conta = conta

        self.label_usuario.configure(
            text=f"Usuário logado:\n{self.email}"
        )