import customtkinter as ctk
from telas.licoes.api_cliente import APICliente
from telas.licoes.midia import GerenciadorMidia
from telas.fundo import FundoEscalavel
class Pesquisa(ctk.CTkFrame):
     
    def __init__(self, master, controlador):
        
        super().__init__(master)
        
        self.controlador = controlador
        self.api = APICliente()
        self.midia = GerenciadorMidia()
        self.fundo = FundoEscalavel(self, "tela de pesquisa.jpeg")
        self.frames = []
        self.frame_atual = 0
        self.duracao = 100
        
        self.criar_componentes()

    def criar_componentes(self):

        ctk.CTkLabel(
            self,
            text="Pesquisa de Sinais",
            font=("Arial", 24, "bold")
        ).pack(pady=20)
        
        self.entrada_pesquisa = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Digite o nome do sinal"
        )
        self.entrada_pesquisa.pack(pady=10)
        
        ctk.CTkButton(
            self,
            text="Pesquisar Sinal",
            command=self.buscar_itens
        ).pack(pady=10)

        self.label_mensagem = ctk.CTkLabel(
            self,
            text="",
            text_color="red"
        )
        self.label_mensagem.pack(pady=5)

        self.frame_modulos = ctk.CTkFrame(self)
        self.frame_modulos.pack(pady=10)

        self.label_gif = ctk.CTkLabel(
            self,
            text=""
        )
        self.label_gif.pack(pady=20)
        
        ctk.CTkButton(
            self,
            text="Voltar ao menu",
            width=200,
            command=lambda: self.controlador.mostrar_tela("menu")
        ).pack(pady=20)
        
    def buscar_itens(self):
        
        for widget in self.frame_modulos.winfo_children():
            widget.destroy()

        self.label_mensagem.configure(text="")

        termo = self.entrada_pesquisa.get().strip()
        
        if not termo:
            self.label_mensagem.configure(
                text="Digite um sinal para pesquisar."
        )
            return
        
        resultado = self.api.chamar(
            "GET",
            f"/pesquisa?termo={termo}"
        )
        if resultado is None:
            self.label_mensagem.configure(
                text="Erro ao consultar a API."
            )
            return

        if len(resultado) == 0:
            self.label_mensagem.configure(
                text="Nenhum sinal correspondente"
            )
            return
        
        for item in resultado:
            
            ctk.CTkButton(
                self.frame_modulos,
                text=item["palavra"],
                width=250,
                command=lambda i=item: self.abrir_sinal(i)
            ).pack(pady=5)
            
    def abrir_sinal(self, item):

        self.frames, self.duracao = self.midia.carregar_frames(
            item["midia"]
        )
        
        if not self.frames:
            self.label_mensagem.configure(
                text="Arquivo de mídia não encontrado."
            )
            return
        
        self.frame_atual = 0
        
        self.label_gif.configure(
            text=item["palavra"],
            compound="top"
        )
        
        self.animar_gif()
        
    def animar_gif(self):
        
        if not self.frames:
            return
        
        self.label_gif.configure(
            image=self.frames[self.frame_atual]
        )
        
        self.frame_atual = (
            self.frame_atual + 1
        ) % len(self.frames)
        
        self.after(
            self.duracao,
            self.animar_gif
        )   