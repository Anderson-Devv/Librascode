import customtkinter as ctk
from tkinter import messagebox
from telas.licoes.api_cliente import APICliente
from telas.fundo import FundoEscalavel

class TelaRevisarSugestoes(ctk.CTkFrame):

    def __init__(self, master, controlador):

        super().__init__(master)

        self.controlador = controlador
        self.api = APICliente()

        self.usuario_id = None
        
        self.fundo = FundoEscalavel(
            self,
            "tela do ranking.jpeg"
        )

        self.criar_componentes()

    def criar_componentes(self):

        ctk.CTkLabel(
            self,
            text="Sugestões Pendentes",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        self.frame_lista = ctk.CTkScrollableFrame(
            self,
            width=900,
            height=500
        )

        self.frame_lista.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        ctk.CTkButton(
            self,
            text="Voltar",
            command=lambda:
                self.controlador.mostrar_tela("menu")
        ).pack(pady=10)

    def configurar_usuario(self, usuario_id):

        self.usuario_id = usuario_id

        self.carregar_sugestoes()

    def carregar_sugestoes(self):

        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        sugestoes = self.api.chamar(
            "GET",
            "/sugestoes/pendentes"
        )

        if not sugestoes:

            ctk.CTkLabel(
                self.frame_lista,
                text="Nenhuma sugestão pendente."
            ).pack(pady=20)

            return

        for sugestao in sugestoes:

            card = ctk.CTkFrame(
                self.frame_lista
            )

            card.pack(
                fill="x",
                pady=10,
                padx=10
            )

            ctk.CTkLabel(
                card,
                text=f"Palavra: {sugestao['palavra']}",
                font=("Arial", 18, "bold")
            ).pack(anchor="w", padx=20)

            ctk.CTkLabel(
                card,
                text=f"Descrição: {sugestao['descricao']}"
            ).pack(anchor="w", padx=20)

            ctk.CTkLabel(
                card,
                text=f"Enviado por: {sugestao['usuario']}"
            ).pack(anchor="w", padx=20)

            botoes = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            botoes.pack(
                pady=10
            )

            ctk.CTkButton(
                botoes,
                text="Aprovar",
                fg_color="green",
                command=lambda sid=sugestao["id"]:
                    self.aprovar(sid)
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                botoes,
                text="Recusar",
                fg_color="red",
                command=lambda sid=sugestao["id"]:
                    self.recusar(sid)
            ).pack(side="left", padx=5)

    def aprovar(self, sugestao_id):

        resposta = self.api.chamar(
            "POST",
            f"/sugestoes/{sugestao_id}/aprovar"
        )

        if resposta:

            messagebox.showinfo(
                "Sucesso",
                resposta["mensagem"]
            )

            self.carregar_sugestoes()
            
    def recusar(self, sugestao_id):

        resposta = self.api.chamar(
            "POST",
            f"/sugestoes/{sugestao_id}/recusar"
        )

        if resposta:

            messagebox.showinfo(
                "Sucesso",
                resposta["mensagem"]
            )

            self.carregar_sugestoes()