import os
import tkinter as tk

import customtkinter as ctk
from PIL import Image, ImageOps, ImageTk

# raiz do projeto / files / midia  (este arquivo está em telas/)
PASTA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "files", "midia"
)

_cache = {}

def montar_imagem(original, largura, altura, modo="cobrir", cor="#101010"):
    if modo == "cobrir":
        return ImageOps.fit(original, (largura, altura), Image.LANCZOS)
    
    imagem = ImageOps.contain(original, (largura, altura), Image.LANCZOS)
    quadro = Image.new("RGB", (largura, altura), cor)
    quadro.paste(imagem, ((largura - imagem.width) // 2, (altura - imagem.height) // 2))
    return quadro

class FundoEscalavel(tk.Label):
    def __init__(self, pai, arquivo, modo="cobrir", cor="#101010", atraso=60):
        
        super().__init__(pai, borderwidth=0, highlightthickness=0)
        self.arquivo = arquivo
        self.modo = modo
        self.cor = cor
        self.atraso = atraso          # ms parados até redesenhar (evita redesenhar a cada pixel)
        self.original = Image.open(os.path.join(PASTA, arquivo)).convert("RGB")
        self.foto = None              # segura a referência (senão o Tk apaga a imagem)
        self.tarefa = None
        self.tamanho = (0, 0)
        
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.bind("<Configure>", self.ao_redimensionar)
    
    def ao_redimensionar(self, evento):
        tamanho = (evento.width, evento.height)
        if tamanho == self.tamanho or min(tamanho) < 2:
            return
        self.tamanho = tamanho
        if self.tarefa is not None:
            self.after_cancel(self.tarefa)
        self.tarefa = self.after(self.atraso, self.redesenhar)
    
    def redesenhar(self):
        self.tarefa = None
        largura, altura = self.tamanho
        chave = (self.arquivo, self.modo, largura, altura)
        if chave not in _cache:
            if len(_cache) > 6:
                _cache.clear()
            imagem = montar_imagem(self.original, largura, altura, self.modo, self.cor)
            _cache[chave] = ImageTk.PhotoImage(imagem)
        self.foto = _cache[chave]
        self.configure(image=self.foto)
        
    def destroy(self):
        if self.tarefa is not None:
            self.after_cancel(self.tarefa)
            self.tarefa = None
        super().destroy()
        
def carregar_fundo(arquivo, largura, altura):
    """Imagem que COBRE largura x altura: recorta o excesso, sem deformar."""
    imagem = Image.open(os.path.join(PASTA, arquivo)).convert("RGB")
    imagem = ImageOps.fit(imagem, (largura, altura), Image.LANCZOS)
    return ctk.CTkImage(light_image=imagem, dark_image=imagem, size=(largura, altura))

def colocar_fundo(janela, imagem):
    """Cria o fundo ATRÁS de tudo: chame antes de criar os outros widgets."""
    fundo = ctk.CTkLabel(janela, text="", image=imagem)
    fundo.place(x=0, y=0, relwidth=1, relheight=1)
    return fundo