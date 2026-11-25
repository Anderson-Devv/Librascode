import os
import shutil
import customtkinter as ctk
from PIL import Image
from tkinter import filedialog
from telas.licoes.api_cliente import APICliente
from tkinter import messagebox

class TelaConquistas(ctk.CTkFrame):

    def __init__(self, master, controlador):

        super().__init__(master)

        self.controlador = controlador
        self.api = APICliente()

        self.usuario_id = None
        self.sticker = None

        self.criar_componentes()

    def criar_componentes(self):

        ctk.CTkLabel(
            self,
            text="Minhas Conquistas",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        self.label_conquista = ctk.CTkLabel(
            self,
            text=""
        )
        self.label_conquista.pack(pady=10)

        self.label_imagem = ctk.CTkLabel(
            self,
            text=""
        )
        self.label_imagem.pack(pady=10)

        self.botao_baixar = ctk.CTkButton(
            self,
            text="Baixar Sticker",
            command=self.baixar_sticker
        )
        self.botao_baixar.pack(pady=10)

        ctk.CTkButton(
            self,
            text="Voltar",
            command=lambda:
            self.controlador.mostrar_tela("menu")
        ).pack(pady=20)

    def configurar_usuario(self, usuario_id):

        self.usuario_id = usuario_id

        self.carregar_conquista()

    def carregar_conquista(self):

        conquistas = self.api.chamar(
            "GET",
            f"/conquistas/{self.usuario_id}"
        )

        if not conquistas:

            self.botao_baixar.configure(
                state="disabled"
            )

            self.label_conquista.configure(
                text="Nenhuma conquista desbloqueada"
            )

            self.label_imagem.configure(
                image=None,
                text=""
            )

            messagebox.showwarning(
                "Conquista Bloqueada",
                "Você ainda não possui conquistas desbloqueadas."
            )

            return
        
        self.botao_baixar.configure(
        state="normal"
        )
                
        ultima = conquistas[-1]

        self.sticker = ultima["sticker"]

        self.label_conquista.configure(
            text=f"{ultima['nome']}\n{ultima['descricao']}"
        )

        caminho = os.path.join(
            "files",
            "stickers",
            self.sticker
        )

        imagem_original = Image.open(caminho)

        largura_original, altura_original = imagem_original.size

        nova_largura = 200
        nova_altura = int(
            altura_original * (nova_largura / largura_original)
        )

        imagem = ctk.CTkImage(
            light_image=imagem_original,
            dark_image=imagem_original,
            size=(nova_largura, nova_altura)
        )
        
        self.label_imagem.configure(
            image=imagem,
            text=""
        )

        self.label_imagem.image = imagem

    def baixar_sticker(self):
        
        if not self.sticker:

            messagebox.showwarning(
            "Conquista Bloqueada",
            "Você ainda não possui nenhuma conquista desbloqueada."
        )

            return

        origem = os.path.join("files", "stickers", self.sticker)

        destino = filedialog.asksaveasfilename(
            initialfile=self.sticker,
            defaultextension=".png"
        )

        if destino:

            shutil.copy(
                origem,
                destino
            )