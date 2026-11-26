import customtkinter as ctk
from telas.fundo import FundoEscalavel
from telas.licoes.api_cliente import APICliente
from tkinter import filedialog, messagebox
from conta.recompensas_certificado import Recompensas
import requests 
class MenuUsuario(ctk.CTkFrame):

    def __init__(self, master, controlador):

        super().__init__(master)

        self.controlador = controlador

        self.fundo = FundoEscalavel(self, "tela do ranking.jpeg")

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
            text="Baixar Guia das Lições",
            width=250,
            command=self.baixar_guia
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Pesquisar Sinais",
            width=250,
            command=self.abrir_pesquisa
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Favoritos",
            width=250,
            command=self.abrir_favoritos
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Ranking",
            width=250,
            command=self.abrir_ranking
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Conquistas",
            width=250,
            command=self.abrir_conquistas
        ).pack(pady=10)
        
        self.botao_sugestao = ctk.CTkButton(
            self,
            text="Enviar Sugestão",
            width=250,
            command=self.abrir_sugestoes
        )

        self.botao_sugestao.pack(pady=10)
        
        self.botao_revisao = ctk.CTkButton(
            self,
            text="Revisar Sugestões",
            width=250,
            command=self.abrir_revisao
        )

        self.botao_revisao.pack(pady=10)
        
        ctk.CTkButton(
            self,
            text="Minhas Sugestões",
            width=250,
            command=self.abrir_minhas_sugestoes
        ).pack(pady=10)
        
        self.botao_certificado = ctk.CTkButton(
            self,
            text="Baixar Certificado",
            width=250,
            command=self.baixar_certificado,
            state="disabled"
        )

        self.botao_certificado.pack(pady=10)

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
            text="Alterar Usuário",
            width=250,
            command=self.alterar_usuario
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

    def fazer_licao(self):

        modulos = self.controlador.telas["modulos"]
        modulos.configurar_usuario(self.usuario_id)
        self.controlador.mostrar_tela("modulos")

    def abrir_ranking(self):
        
        ranking = self.controlador.telas["ranking"]
        ranking.configurar_usuario(self.usuario_id)
        self.controlador.mostrar_tela("ranking")
        
    def abrir_pesquisa(self):

        pesquisa = self.controlador.telas["pesquisa"]

        pesquisa.configurar_usuario(
            self.usuario_id
        )

        self.controlador.mostrar_tela(
            "pesquisa"
        )
        
    def abrir_conquistas(self):

        conquistas = self.controlador.telas["conquistas"]

        conquistas.configurar_usuario(
        self.usuario_id
        )

        self.controlador.mostrar_tela(
        "conquistas"
        )
    def alterar_senha(self):

        self.conta.alterar_senha()

    def alterar_email(self):

        if self.conta.alterar_email():
            self.email = self.conta.email
            self.label_usuario.configure(
                text=f"Usuário logado:\n{self.usuario}"
            )

    def deletar_conta(self):

        if self.conta.deletar_conta():
            self.controlador.mostrar_tela("login")
        
    def configurar_usuario(self, email, usuario, usuario_id, conta):
        self.email = email
        self.usuario = usuario
        self.usuario_id = usuario_id
        self.conta = conta
        self.label_usuario.configure(
            text=f"Usuário logado:\n{self.usuario}"
        )
        self.verificar_certificado()
        self.verificar_permissoes()
        
        
    def alterar_usuario(self):
        if self.conta.alterar_usuario():
            self.novo_usuario = self.conta.usuario
            self.label_usuario.configure(
                text=f"Usuário logado:\n{self.usuario}"
        )
    def abrir_favoritos(self):

        favoritos = self.controlador.telas["favoritos"]

        favoritos.configurar_usuario(
            self.usuario_id
        )

        self.controlador.mostrar_tela(
            "favoritos"
        )
        
    def verificar_certificado(self):
        resposta = APICliente().chamar(
            "GET",
            f"/certificado/{self.usuario_id}"
        )

        if resposta and resposta["liberado"]:

            self.botao_certificado.configure(
                state="normal"
            )

        else:
            self.botao_certificado.configure(
                state="disabled"
            )
            
    def baixar_certificado(self):

        recompensas = Recompensas()

        ranking = APICliente().chamar(
            "GET",
            "/ranking"
        )

        pontos = 0

        for usuario in ranking:

            if usuario["usuario_id"] == self.usuario_id:

                pontos = usuario["pontos"]
                break

        caminho = recompensas.gerar_certificado(
            self.usuario,
            pontos
        )

        if caminho:

            messagebox.showinfo(
                "Certificado",
                "Certificado salvo com sucesso!"
            )
            
    def baixar_guia(self):

        resposta = requests.get(
            "http://127.0.0.1:5000/guia"
        )

        destino = filedialog.asksaveasfilename(
            initialfile="guia_licoes.pdf",
            defaultextension=".pdf"
        )

        if not destino:
            return

        with open(destino, "wb") as arquivo:
            arquivo.write(resposta.content)

        messagebox.showinfo(
            "Sucesso",
            "Guia baixado com sucesso!"
        )
        
    def abrir_sugestoes(self):

        tela = self.controlador.telas["enviar_sugestao"]

        tela.configurar_usuario(
            self.usuario_id
        )

        self.controlador.mostrar_tela(
            "enviar_sugestao"
        )
        
    def abrir_revisao(self):

        tela = self.controlador.telas[
            "revisar_sugestoes"
        ]

        tela.configurar_usuario(
            self.usuario_id
        )

        self.controlador.mostrar_tela(
            "revisar_sugestoes"
        )
        
    def abrir_minhas_sugestoes(self):

        tela = self.controlador.telas[
            "minhas_sugestoes"
        ]

        tela.configurar_usuario(
            self.usuario_id
        )

        self.controlador.mostrar_tela(
            "minhas_sugestoes"
        )
        
    def verificar_permissoes(self):

        resposta = APICliente().chamar(
            "GET",
            f"/nivel/{self.usuario_id}"
        )

        if not resposta:
            return

        nivel = resposta["nivel"]

        if nivel == "Usuario":

            self.botao_sugestao.pack_forget()
            self.botao_revisao.pack_forget()

        elif nivel in ["Bronze", "Prata"]:

            self.botao_sugestao.pack(pady=10)

            self.botao_revisao.pack_forget()

        elif nivel in [
            "Ouro",
            "Diamante",
            "Administrador"
        ]:

            self.botao_sugestao.pack(pady=10)
            self.botao_revisao.pack(pady=10)