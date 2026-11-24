import customtkinter as ctk
from tkinter import messagebox
from telas.licoes.api_cliente import APICliente


class TelaFavoritos(ctk.CTkFrame):

    def __init__(self, master, controlador):

        super().__init__(master)

        self.controlador = controlador
        self.api = APICliente()
        self.usuario_id = None

        self.criar_componentes()

    def criar_componentes(self):

        ctk.CTkLabel(
            self,
            text="Meus Favoritos",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        self.frame_favoritos = ctk.CTkFrame(self)
        self.frame_favoritos.pack(
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

        self.carregar_favoritos()
        
    def carregar_favoritos(self):

        for widget in self.frame_favoritos.winfo_children():
            widget.destroy()

        favoritos = self.api.chamar(
            "GET",
            f"/favoritos/{self.usuario_id}"
        )

        if not favoritos:

            messagebox.showinfo(
                "Favoritos",
                "Você ainda não possui sinais favoritos."
            )

            ctk.CTkLabel(
                self.frame_favoritos,
                text="Nenhum favorito cadastrado."
            ).pack(pady=20)

            return

        for sinal in favoritos:

            ctk.CTkLabel(
                self.frame_favoritos,
                text=sinal["palavra"],
                font=("Arial", 16)
            ).pack(pady=5)