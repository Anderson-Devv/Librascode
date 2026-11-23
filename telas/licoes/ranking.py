import customtkinter as ctk
from telas.licoes.api_cliente import APICliente
from telas.fundo import FundoEscalavel

class TelaRanking(ctk.CTkFrame):
    
    def __init__(self, master, controlador):
        
        super().__init__(master)
        
        self.controlador = controlador
        self.usuario_id = None
        
        self.montar_ranking()
        
    def montar_ranking(self):
        
        FundoEscalavel(self, "500x400.jpeg")

        cartao = ctk.CTkFrame(self, corner_radius=16)
        cartao.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(
            cartao,
            text="Ranking",
            font=("Arial", 28, "bold")
        ).pack(padx=40, pady=(20, 10))
        
        self.label_mensagem = ctk.CTkLabel(
            cartao,
            text="",
            text_color="red"
        )
        self.label_mensagem.pack(pady=5)
        
        # as linhas do ranking ficam aqui dentro: a cada abertura são apagadas e refeitas
        self.frame_linhas = ctk.CTkFrame(cartao, fg_color="transparent")
        self.frame_linhas.pack(pady=10)
        
        self.label_posicao = ctk.CTkLabel(
            cartao,
            text="",
            font=("Arial", 15, "bold")
        )
        self.label_posicao.pack(pady=(10, 5))
        
        ctk.CTkButton(
            cartao,
            text="Voltar ao menu",
            width=200,
            command=lambda: self.controlador.mostrar_tela("menu")
        ).pack(pady=(10, 20))
    
    def carregar_ranking(self):
        
        for widget in self.frame_linhas.winfo_children():
            widget.destroy()

        self.label_mensagem.configure(text="")
        self.label_posicao.configure(text="")
        
        ranking = APICliente().chamar("GET", "/ranking")

        if ranking is None:
            ctk.CTkLabel(
                self.frame_linhas,
                text="Erro ao carregar o ranking.",
                font=("Arial", 16)
            ).pack(pady=20)
            return

        if not ranking:
            ctk.CTkLabel(
                self.frame_linhas,
                text="Ninguém pontuou ainda.\nFaça uma lição para entrar no ranking!",
                font=("Arial", 16),
            ).pack(pady=20)

        # procura a linha do usuário logado
        minha = None
        for linha in ranking:
            if linha["usuario_id"] == self.usuario_id:
                minha = linha

        # mostra o top 10 e destaca o usuário logado
        for linha in ranking[:10]:
            eu = linha["usuario_id"] == self.usuario_id
            texto = f"{linha['ranking']}º   {linha['usuario']}   -   {linha['acertos']} acertos"
            if eu:
                texto += "   (você)"
            label = ctk.CTkLabel(self.frame_linhas, text=texto, font=("Arial", 16))
            label.pack(pady=3)
            if eu:
                label.configure(text_color="gold")

        # se o usuário ficou fora do top 10, mostra a posição dele embaixo
        if ranking:
            if minha is None:
                mensagem = "Você ainda não tem acertos."
            elif minha not in ranking[:10]:
                mensagem = f"Sua posição: {minha['ranking']}º  ({minha['acertos']} acertos)"
            else:
                mensagem = ""
            self.label_posicao.configure(text=mensagem)

    def configurar_usuario(self, usuario_id):

        self.usuario_id = usuario_id

        self.carregar_ranking()
