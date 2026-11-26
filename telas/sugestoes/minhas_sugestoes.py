import customtkinter as ctk
from telas.licoes.api_cliente import APICliente
from telas.fundo import FundoEscalavel


class TelaMinhasSugestoes(ctk.CTkFrame):

    def __init__(self, master, controlador):

        super().__init__(master)

        self.controlador = controlador
        self.api = APICliente()

        self.usuario_id = None
        
        self.fundo = FundoEscalavel(
            self,
            "cartão librascode.jpeg"
        )

        self.criar_componentes()

    def criar_componentes(self):

        ctk.CTkLabel(
            self,
            text="Minhas Sugestões",
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
            f"/minhas-sugestoes/{self.usuario_id}"
        )

        if not sugestoes:

            ctk.CTkLabel(
                self.frame_lista,
                text="Você ainda não enviou sugestões."
            ).pack(pady=20)

            return
        
        for sugestao in sugestoes:

            card = ctk.CTkFrame(
                self.frame_lista
            )

            card.pack(
                fill="x",
                padx=10,
                pady=10
            )

            ctk.CTkLabel(
                card,
                text=sugestao["palavra"],
                font=("Arial", 18, "bold")
            ).pack(anchor="w", padx=20, pady=5)
            
            status = sugestao["status"]

            status = sugestao["status"]

            if status == "Aprovado":

                texto_status = "✅ Aprovado"
                cor = "lightgreen"

            elif status == "Recusado":

                texto_status = "❌ Recusado"
                cor = "red"

            else:

                texto_status = "⏳ Pendente"
                cor = "gold"
                
            ctk.CTkLabel(
                card,
                text=texto_status,
                text_color=cor
            ).pack(anchor="w", padx=20)

            ctk.CTkLabel(
                card,
                text=sugestao["descricao"],
                wraplength=700
            ).pack(anchor="w", padx=20, pady=5)

            ctk.CTkLabel(
                card,
                text=f"Data: {sugestao['data_envio']}"
            ).pack(anchor="w", padx=20, pady=5)