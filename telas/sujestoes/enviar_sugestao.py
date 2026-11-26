import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from telas.licoes.api_cliente import APICliente
from telas.fundo import FundoEscalavel

class TelaEnviarSugestao(ctk.CTkFrame):

    def __init__(self, master, controlador):

        super().__init__(master)

        self.controlador = controlador
        self.api = APICliente()

        self.usuario_id = None
        self.caminho_midia = ""

        self.fundo = FundoEscalavel(
            self,
            "tela de pesquisa.jpeg"
        )

        self.criar_componentes()

    def criar_componentes(self):

        ctk.CTkLabel(
            self,
            text="Enviar Sugestão",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        ctk.CTkLabel(
            self,
            text="Palavra"
        ).pack()

        self.campo_palavra = ctk.CTkEntry(
            self,
            width=300
        )

        self.campo_palavra.pack(pady=5)

        ctk.CTkLabel(
            self,
            text="Módulo"
        ).pack()

        self.combo_modulo = ctk.CTkComboBox(
            self,
            width=300,
            values=[]
        )

        self.combo_modulo.pack(pady=5)

        ctk.CTkLabel(
            self,
            text="Descrição"
        ).pack()

        self.campo_descricao = ctk.CTkTextbox(
            self,
            width=350,
            height=100
        )

        self.campo_descricao.pack(pady=5)

        self.label_arquivo = ctk.CTkLabel(
            self,
            text="Nenhum arquivo selecionado"
        )

        self.label_arquivo.pack(pady=5)

        ctk.CTkButton(
            self,
            text="Selecionar GIF",
            command=self.selecionar_arquivo
        ).pack(pady=5)

        ctk.CTkButton(
            self,
            text="Enviar Sugestão",
            fg_color="green",
            command=self.enviar_sugestao
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Voltar",
            command=lambda:
                self.controlador.mostrar_tela("menu")
        ).pack(pady=10)

    def configurar_usuario(self, usuario_id):

        self.usuario_id = usuario_id

        self.carregar_modulos()

    def carregar_modulos(self):

        modulos = self.api.chamar(
            "GET",
            "/modulos"
        )

        if not modulos:
            return

        self.modulos = {
            modulo["nome"]: modulo["id"]
            for modulo in modulos
        }

        self.combo_modulo.configure(
            values=list(self.modulos.keys())
        )

        if self.modulos:
            primeiro = next(
                iter(self.modulos)
            )

            self.combo_modulo.set(primeiro)

    def selecionar_arquivo(self):

        arquivo = filedialog.askopenfilename(
            title="Selecionar GIF",
            filetypes=[
                ("GIF", "*.gif"),
                ("Todos os Arquivos", "*.*")
            ]
        )

        if arquivo:

            self.caminho_midia = arquivo

            self.label_arquivo.configure(
                text=os.path.basename(
                    arquivo
                )
            )

    def enviar_sugestao(self):

        palavra = self.campo_palavra.get().strip()

        descricao = self.campo_descricao.get(
            "1.0",
            "end"
        ).strip()

        modulo_nome = self.combo_modulo.get()

        if not palavra:

            messagebox.showerror(
                "Erro",
                "Informe uma palavra."
            )

            return

        if not self.caminho_midia:

            messagebox.showerror(
                "Erro",
                "Selecione um GIF."
            )

            return

        modulo_id = self.modulos[
            modulo_nome
        ]

        resposta = self.api.chamar(
            "POST",
            "/sugestoes",
            json={
                "usuario_id": self.usuario_id,
                "palavra": palavra,
                "descricao": descricao,
                "modulo_id": modulo_id,
                "midia": self.caminho_midia
            }
        )

        if resposta:

            messagebox.showinfo(
                "Sucesso",
                "Sugestão enviada para análise."
            )

            self.campo_palavra.delete(
                0,
                "end"
            )

            self.campo_descricao.delete(
                "1.0",
                "end"
            )

            self.label_arquivo.configure(
                text="Nenhum arquivo selecionado"
            )

            self.caminho_midia = ""