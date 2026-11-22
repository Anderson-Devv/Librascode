from pathlib import Path
from PIL import Image
import customtkinter as ctk


class GerenciadorFundos:

    PASTA_FUNDOS = (
        Path(__file__).resolve().parent.parent
        / "files"
        / "midia"
        / "fundos"
    )

    @classmethod
    def aplicar(cls, tela, caminho_imagem):

        caminho_completo = cls.PASTA_FUNDOS / caminho_imagem

        with Image.open(caminho_completo) as arquivo:
            imagem_original = arquivo.convert("RGB")

        fundo = ctk.CTkLabel(tela, text="")
        fundo.place(x=0, y=0, relwidth=1, relheight=1)
        #fundo.lower()

        ultimo_tamanho = None

        def redimensionar(event=None):

            nonlocal ultimo_tamanho

            largura = tela.winfo_width()
            altura = tela.winfo_height()

            if largura <= 1 or altura <= 1:
                return

            if ultimo_tamanho == (largura, altura):
                return

            ultimo_tamanho = (largura, altura)

            proporcao = min(
                largura / imagem_original.width,
                altura / imagem_original.height
            )

            nova_largura = round(imagem_original.width * proporcao)
            nova_altura = round(imagem_original.height * proporcao)

            imagem = imagem_original.resize(
                (nova_largura, nova_altura),
                Image.Resampling.LANCZOS
            )


            foto = ctk.CTkImage(
                light_image=imagem,
                dark_image=imagem,
                size=(largura, altura)
            )

            fundo.configure(image=foto)
            fundo.imagem = foto

            print("Imagem configurada!")
            print("Dimensões da imagem:", imagem.size)

        tela.bind("<Configure>", redimensionar, add="+")

        tela.after(100, redimensionar)

        return fundo