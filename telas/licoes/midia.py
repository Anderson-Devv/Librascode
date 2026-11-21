
import os
import customtkinter as ctk

from PIL import Image, ImageSequence


class GerenciadorMidia:

    def __init__(self):

        self.pasta_midia = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__)
                    )
                )
            ),
            "files",
            "midia"
        )

        self.tamanho = (220, 220)


    def carregar_frames(self, arquivo):

        caminho = os.path.join(
            self.pasta_midia,
            arquivo
        )

        if not os.path.isfile(caminho):
            return [], 100

        imagem = Image.open(caminho)

        duracao = imagem.info.get("duration", 100) or 100

        frames = []

        for quadro in ImageSequence.Iterator(imagem):

            quadro = quadro.convert("RGBA").resize(
                self.tamanho
            )

            frames.append(
                ctk.CTkImage(
                    light_image=quadro,
                    dark_image=quadro,
                    size=self.tamanho
                )
            )

        imagem.close()

        return frames, duracao
