
import customtkinter as ctk
from telas.gerenciador_fundos import GerenciadorFundos

# from telas.Licoes.ranking import TelaRanking


class MenuUsuario(ctk.CTkFrame):

    def __init__(self, master, controlador):

        super().__init__(master)

        self.controlador = controlador

        self.email = None
        self.usuario_id = None
        self.conta = None

        self.criar_componentes()

    def criar_componentes(self):

        self.imagem_fundo = GerenciadorFundos.aplicar(
            self,
            "cartao_librascode.jpeg"
        )


        self.label_mensagem = ctk.CTkLabel(
        self,
        text="",
        text_color="red"
        )


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
            text="Meu perfil",
            width=250,
            command=self.abrir_perfil
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

    def abrir_perfil(self):

        tela = self.controlador.telas["perfil"]

        tela.configurar_perfil(
            self.usuario_id,
            self.conta
        )

        self.controlador.mostrar_tela("perfil")

    def atualizar_usuario(self):

        self.label_usuario.configure(
            text=f"Usuário: {self.conta.usuario}"
        )

    def configurar_usuario(self, email, usuario_id, conta):
        self.email = email
        self.usuario_id = usuario_id
        self.conta = conta

        self.label_usuario.configure(
            text=f"Usuário logado:\n{self.conta.usuario}"
        )

