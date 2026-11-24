import customtkinter as ctk
from telas.licoes.api_cliente import APICliente
from telas.fundo import FundoEscalavel
class TelaModulos(ctk.CTkFrame):

    def __init__(self, master, controlador):

        super().__init__(master)

        self.controlador = controlador
        self.usuario_id = None
        
        self.fundo = FundoEscalavel(self, "500x400.jpeg")
        self.api = APICliente()

        self.criar_componentes()

    def criar_componentes(self):

        ctk.CTkLabel(
            self,
            text="Escolha um módulo",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        self.label_mensagem = ctk.CTkLabel(
            self,
            text="",
            text_color="red"
        )
        self.label_mensagem.pack(pady=5)

        self.frame_modulos = ctk.CTkFrame(self)
        self.frame_modulos.pack(pady=10)
        
        ctk.CTkButton(
            self,
            text="Voltar ao menu",
            width=200,
            command=lambda: self.controlador.mostrar_tela("menu")
        ).pack(pady=20)

    def carregar_modulos(self):

        for widget in self.frame_modulos.winfo_children():
            widget.destroy()

        self.label_mensagem.configure(text="")

        self.modulos = self.api.chamar(
            "GET",
            "/modulos"
        )

        if self.modulos is None:
            self.label_mensagem.configure(
                text="Não foi possível carregar os módulos."
            )
            return

        for modulo in self.modulos:

            ctk.CTkButton(
                self.frame_modulos,
                text=f"{modulo['nome']} ({modulo['total_sinais']} sinais)",
                width=320,
                height=45,
                command=lambda mid=modulo["id"]: self.iniciar(mid)
            ).pack(pady=8)

    def iniciar(self, modulo_id):

        self.controlador.telas["licao"].configurar_licao(
            self.usuario_id,
            modulo_id
        )

        self.controlador.mostrar_tela("licao")

    def configurar_usuario(self, usuario_id):

        self.usuario_id = usuario_id

        self.carregar_modulos()
        