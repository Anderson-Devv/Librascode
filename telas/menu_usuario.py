
import customtkinter as ctk
from telas.gerenciador_fundos import GerenciadorFundos

# from telas.Licoes.modulo import TelaModulos
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
            text="Alterar Senha",
            width=250,
            command=self.alterar_senha
            ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Alterar Email",
            width=250,
            command=lambda: self.alterar_email()
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

    def alterar_senha(self):

        self.label_mensagem.pack_forget()

        resultado = self.conta.alterar_senha()

        if resultado == "senha_invalida":
            mensagem = "A senha deve ter entre 8 e 15 caracteres."
            cor = "red"

        elif resultado == "senhas_diferentes":
            mensagem = "As senhas não coincidem!"
            cor = "red"

        elif resultado is True:
            mensagem = "Senha alterada com sucesso!"
            cor = "green"

        elif resultado == "senha_usada":
            mensagem = "Esta senha ja esta sendo usada."
            cor = "red"

        elif resultado is False:
            mensagem = "Erro ao alterar senha."
            cor = "red"

        else:
            return

        self.label_mensagem.configure(
            text=mensagem,
            text_color=cor
        )

        self.label_mensagem.pack(pady=3)

    def alterar_email(self):

        self.label_mensagem.pack_forget()

        resultado = self.conta.alterar_email()

        if resultado == "email_invalido":
            mensagem = "Seu email precisa ter @ufrpe.br no final"
            cor = "red"

        elif resultado == "email_igual":
            mensagem = "Você ja está usando esse email"
            cor = "red"

        elif resultado is False:
            mensagem = "Erro ao trocar email"
            cor = "red"

        else:
            mensagem = "Email trocado com Sucesso"
            cor = "green"

        self.label_mensagem.configure(
            text=mensagem,
            text_color = cor
        )
        self.label_mensagem.pack(pady = 3)

    def configurar_usuario(self, email, usuario_id, conta):
        self.email = email
        self.usuario_id = usuario_id
        self.conta = conta

        self.label_usuario.configure(
            text=f"Usuário logado:\n{self.email}"
        )

