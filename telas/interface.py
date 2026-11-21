
import customtkinter as ctk

from telas.tela_login import TelaLogin
from telas.menu_usuario import MenuUsuario
from telas.tela_cadastro import TelaCadastro
from telas.licoes.modulo import TelaModulos
from telas.tela_licao import TelaLicao

class Interface:

    def __init__(self):

        self.janela = ctk.CTk()
        self.janela.title("LibrasCode")
        self.janela.geometry("900x600")

        self.container = ctk.CTkFrame(self.janela)
        self.container.pack(fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.telas = {}

        self.adicionar_tela("login", TelaLogin)
        self.adicionar_tela("menu", MenuUsuario)
        self.adicionar_tela("cadastro", TelaCadastro )
        self.adicionar_tela("modulos", TelaModulos)
        self.adicionar_tela("licao", TelaLicao)
        self.mostrar_tela("login")

    def adicionar_tela(self, nome, classe_tela):

        tela = classe_tela(self.container, self)

        tela.grid(row=0, column=0, sticky="nsew")

        self.telas[nome] = tela

    def mostrar_tela(self, nome):

        tela = self.telas[nome]
        tela.tkraise()

    def executar(self):

        self.janela.mainloop()

if __name__ == "__main__":
    app = Interface()
    app.executar()