import customtkinter as ctk
from PIL import Image
from telas.fundo import FundoEscalavel
from telas.licoes.api_cliente import APICliente
from telas.licoes.midia import GerenciadorMidia
class TelaLicao(ctk.CTkFrame):

    def __init__(self, master, controlador):

        super().__init__(master)
        
        self.controlador = controlador
        self.usuario_id = None
        self.modulo_id = None
        
        self.fundo = FundoEscalavel(self, "tela do ranking.jpeg")
        
        self.api = APICliente()
        self.midia = GerenciadorMidia()

        self.imagem_vazia = Image.new(
            "RGBA", (1, 1), (0, 0, 0, 0)
        )

        self.vazio = ctk.CTkImage(
            light_image=self.imagem_vazia,
            dark_image=self.imagem_vazia,
            size=(1, 1)
        )

        self.criar_componentes()
        self.bind("<Destroy>", self.ao_destruir)

    def criar_componentes(self):

        self.label_titulo = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 20, "bold")
        )
        self.label_titulo.pack(pady=(20, 5))

        self.label_enunciado = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 18)
        )
        self.label_enunciado.pack(pady=5)

        self.label_midia = ctk.CTkLabel(self, text="")
        self.label_midia.pack(pady=5)

        self.frame_opcoes = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.frame_opcoes.pack(pady=2)

        self.label_feedback = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 15, "bold"),
            wraplength=500
        )
        self.label_feedback.pack(pady=3)

        self.botao_proximo = ctk.CTkButton(
            self,
            text="Próxima",
            width=200,
            command=self.proxima
        )

        self.frame_resultado = ctk.CTkFrame(self)

        self.label_resultado = ctk.CTkLabel(
            self.frame_resultado,
            text="Lição concluída!",
            font=("Arial", 30, "bold")
        )

        self.label_resultado.pack(pady=40)

        self.label_estatisticas = ctk.CTkLabel(
            self.frame_resultado,
            text="",
            font=("Arial", 22)
        )

        self.label_estatisticas.pack(pady=20)

        ctk.CTkButton(
            self.frame_resultado,
            text="Voltar ao menu",
            width=200,
            command=lambda: self.controlador.mostrar_tela("menu")
        ).pack(pady=20)

    def parar_animacao(self):

        if not hasattr(self, "estado"):
            return

        if self.estado["job"] is not None:
            try:
                self.after_cancel(self.estado["job"])
            except Exception:
                pass

            self.estado["job"] = None

    def animar(self, duracao):

        self.label_midia.configure(
            image=self.estado["frames"][self.estado["quadro"]]
        )

        self.estado["quadro"] = (
            self.estado["quadro"] + 1
        ) % len(self.estado["frames"])

        if len(self.estado["frames"]) > 1:
            self.estado["job"] = self.after(
                duracao,
                self.animar,
                duracao
            )

    def mostrar_midia(self, arquivo):

        self.parar_animacao()

        frames, duracao = self.midia.carregar_frames(arquivo)

        if not frames:
            self.label_midia.configure(
                text=f"[mídia não encontrada: {arquivo}]",
                image=self.vazio
            )
            return

        self.estado["frames"] = frames
        self.estado["quadro"] = 0

        self.label_midia.configure(text="")

        self.animar(duracao)


    def ao_destruir(self, evento):

        if evento.widget is self:
            self.parar_animacao()    

    def mostrar_questao(self):

        q = self.questoes[self.estado["indice"]]

        self.label_titulo.configure(
            text=f"Questão {self.estado['indice'] + 1} de {len(self.questoes)}"
        )

        self.label_enunciado.configure(text=q["enunciado"])

        self.mostrar_midia(q["midia"])

        self.label_feedback.configure(text="")
        self.botao_proximo.pack_forget()

        for widget in self.frame_opcoes.winfo_children():
            widget.destroy()

        self.estado["botoes"] = []

        for opcao in q["opcoes"]:

            botao = ctk.CTkButton(
                self.frame_opcoes,
                text=opcao,
                width=300,
                height=40,
                command=lambda o=opcao: self.responder(o),
            )

            botao.pack(pady=5)

            self.estado["botoes"].append(botao)

    def responder(self, opcao):
        q = self.questoes[self.estado["indice"]]
        resultado = self.api.chamar(
            "POST",
            "/respostas",
            json={
                "usuario_id": self.usuario_id,
                "sinal_id": q["sinal_id"],
                "resposta": opcao,
            },
        )        
        if resultado is None:
            return
        print("Resposta recebida:", resultado)

        for botao in self.estado["botoes"]:
            botao.configure(state="disabled")
            if botao.cget("text") == resultado["correta"]:
                botao.configure(fg_color="green")
            elif botao.cget("text") == opcao:
                botao.configure(fg_color="red")

        if resultado["acertou"]:
            self.estado["acertos"] += 1
            self.estado["pontos"] += resultado["pontos"]
            self.label_feedback.configure(
                text=f"Acertou! +{resultado['pontos']} pontos", text_color="lightgreen"
            )
        else:
            self.label_feedback.configure(
                text=f"Errou. Era: {resultado['correta']}", text_color="salmon"
            )

        ultima = self.estado["indice"] == len(self.questoes) - 1
        self.botao_proximo.configure(
            text="Finalizar" if ultima else "Próxima"
        )

        self.botao_proximo.pack(
            pady=5
        )        
        print("Botão próxima foi exibido!")

    def proxima(self):

        print("Método próxima foi chamado!")

        self.estado["indice"] += 1

        if self.estado["indice"] >= len(self.questoes):
            self.finalizar()
        else:
            self.mostrar_questao()
    
    def finalizar(self):
        
        self.api.chamar(
            "POST",
            "/historico",
            json={
                "usuario_id": self.usuario_id,
                "modulo_id": self.modulo_id,
                "pontuacao": self.estado["pontos"]
            }
        )
            
        self.parar_animacao()
        
        self.label_titulo.pack_forget()
        self.label_enunciado.pack_forget()
        self.label_midia.pack_forget()
        self.frame_opcoes.pack_forget()
        self.label_feedback.pack_forget()
        self.botao_proximo.pack_forget()
        
        self.label_estatisticas.configure(
            text=f"Acertos: {self.estado['acertos']} de {len(self.questoes)}\n"
                 f"Pontos ganhos: {self.estado['pontos']}"
        )
        
        self.frame_resultado.pack(pady=20)

    def configurar_licao(self, usuario_id, modulo_id):

        self.parar_animacao()
    
        self.usuario_id = usuario_id
        self.modulo_id = modulo_id

        self.preparar_nova_licao()

        self.label_titulo.configure(text="")
        self.label_enunciado.configure(text="")
        self.label_feedback.configure(text="")
        self.label_midia.configure(text="", image=self.vazio)

        self.botao_proximo.pack_forget()

        for widget in self.frame_opcoes.winfo_children():
            widget.destroy()

        dados = self.api.chamar(
            "GET",
            f"/modulos/{modulo_id}/licao",
            params={"qtd": 5}
        )

        if dados is None:
            return

        self.questoes = dados["questoes"]

        if not self.questoes:
            self.label_enunciado.configure(
                text="Não existem questões neste módulo."
            )
            return

        self.estado = {
            "indice": 0,
            "acertos": 0,
            "pontos": 0,
            "frames": [],
            "quadro": 0,
            "job": None,
            "botoes": []
        }

        self.mostrar_questao()

    def preparar_nova_licao(self):

        self.frame_resultado.pack_forget()

        self.label_titulo.pack(pady=(20, 5))
        self.label_enunciado.pack(pady=5)
        self.label_midia.pack(pady=5)
        self.frame_opcoes.pack(pady=2)
        self.label_feedback.pack(pady=3)

        self.botao_proximo.pack_forget()