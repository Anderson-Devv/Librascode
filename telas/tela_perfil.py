import customtkinter as ctk

from telas.licoes.api_cliente import APICliente
from telas.gerenciador_fundos import GerenciadorFundos


class TelaPerfil(ctk.CTkFrame):

    def __init__(self, master, controlador):
        super().__init__(master)

        self.controlador = controlador
        self.api = APICliente()

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


        self.label_nome = ctk.CTkLabel(
            self,
            text="",
            fg_color="transparent"
        )
        self.label_nome.pack(pady=10)

        self.label_email = ctk.CTkLabel(
            self,
            text="",
            fg_color="transparent"
        )
        self.label_email.pack(pady=10)

        self.label_historico = ctk.CTkLabel(
            self,
            text="Módulos realizados",
            font=("Arial", 18, "bold"),
            fg_color="transparent"
        )
        self.label_historico.pack(pady=10)

        self.frame_modulos = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.frame_modulos.pack(pady=5)

        self.botao_usuario = ctk.CTkButton(
            self,
            text="Alterar usuário",
            command=self.alterar_usuario
        )
        self.botao_usuario.pack(pady=5)

        self.botao_email = ctk.CTkButton(
            self,
            text="Alterar e-mail",
            command=self.alterar_email
        )
        self.botao_email.pack(pady=5)

        self.botao_senha = ctk.CTkButton(
            self,
            text="Alterar senha",
            command=self.alterar_senha
        )
        self.botao_senha.pack(pady=5)

        self.botao_voltar = ctk.CTkButton(
            self,
            text="Voltar",
            command=self.voltar_menu        
            )
        self.botao_voltar.pack(pady=5)

    def configurar_perfil(self, usuario_id, conta):

        self.usuario_id = usuario_id
        self.conta = conta

        dados = self.api.buscar_perfil(usuario_id)

        if dados is None:
            return

        self.label_nome.configure(
            text=dados["usuario"]
        )

        self.label_email.configure(
            text=dados["email"]
        )

        for widget in self.frame_modulos.winfo_children():
            widget.destroy()

        for modulo in dados["modulos"]:

            texto = (
                f'{modulo["nome"]}: '
                f'{modulo["vezes_realizado"]} vez(es) realizado'
            )

            label = ctk.CTkLabel(
                self.frame_modulos,
                text=texto,
                fg_color="transparent"
            )

            label.pack(pady=3)

    def alterar_usuario(self):

        self.label_mensagem.pack_forget()

        resultado = self.conta.alterar_usuario()

        if resultado is False:
            mensagem = "Erro ao mudar nome de usuário"
            cor = "red"

        elif resultado == "nome_invalido":
            mensagem = "O usuário deve conter de 3 a 15 caracteres"
            cor = "red"

        elif resultado == "usuario_igual":
            mensagem = "Este já é o seu nome de usuário"
            cor = "red"

        elif resultado == "usuario_nao_encontrado":
            mensagem = "Usuário não encontrado no banco"
            cor = "red"

        elif resultado == "erro_bd":
            mensagem = "Erro ao atualizar o banco de dados"
            cor = "red"

        elif resultado is True:

            self.configurar_perfil(
                self.usuario_id,
                self.conta
            )

            mensagem = "Usuário alterado com sucesso!"
            cor = "green"

        else:
            return

        self.label_mensagem.configure(
            text=mensagem,
            text_color=cor
        )

        self.label_mensagem.pack(pady=3)

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
            mensagem = "Você já está usando esse email"
            cor = "red"

        elif resultado is False:
            mensagem = "Erro ao trocar email"
            cor = "red"

        elif resultado is True:

            self.configurar_perfil(
                self.usuario_id,
                self.conta
            )

            mensagem = "Email trocado com sucesso!"
            cor = "green"

        else:
            mensagem = "Não foi possível alterar o email"
            cor = "red"

        self.label_mensagem.configure(
            text=mensagem,
            text_color=cor
        )

        self.label_mensagem.pack(pady=3)

    def voltar_menu(self):

        menu = self.controlador.telas["menu"]

        menu.atualizar_usuario()

        self.controlador.mostrar_tela("menu")
