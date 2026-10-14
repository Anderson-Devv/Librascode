"""
Telas das lições e do ranking (customtkinter), SEM classes: só funções.
Conversa com a API em api_librascode.py.
Depende de: pip install requests customtkinter pillow
"""
import os
from tkinter import messagebox

import customtkinter as ctk
import requests
from PIL import Image, ImageSequence

API = "http://127.0.0.1:5000"
PASTA_MIDIA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "midia")
TAMANHO_MIDIA = (320, 320)


def chamar_api(metodo, rota, **kwargs):
    try:
        resposta = requests.request(metodo, API + rota, timeout=5, **kwargs)
        resposta.raise_for_status()
        return resposta.json()
    except requests.RequestException:
        messagebox.showerror(
            "Erro", "Não foi possível falar com a API. O api_librascode.py está rodando?"
        )
        return None


def carregar_frames(arquivo, tamanho=TAMANHO_MIDIA):
    """Devolve (lista de quadros, duração de cada quadro em ms).
    PNG/JPG vira 1 quadro; GIF vira vários. Se o arquivo não existe, devolve lista vazia."""
    caminho = os.path.join(PASTA_MIDIA, arquivo)
    if not os.path.isfile(caminho):
        return [], 100

    imagem = Image.open(caminho)
    duracao = imagem.info.get("duration", 100) or 100
    frames = []
    for quadro in ImageSequence.Iterator(imagem):
        quadro = quadro.convert("RGBA").resize(tamanho)
        frames.append(ctk.CTkImage(light_image=quadro, dark_image=quadro, size=tamanho))
    return frames, duracao


# ---------- módulos ----------

def abrir_modulos(janela_pai, usuario_id):
    modulos = chamar_api("GET", "/modulos")
    if modulos is None:
        return

    janela = ctk.CTkToplevel(janela_pai)
    janela.title("Módulos")
    janela.geometry("500x500")

    ctk.CTkLabel(janela, text="Escolha um módulo", font=("Arial", 24, "bold")).pack(pady=20)

    def iniciar(modulo_id):
        janela.destroy()
        abrir_licao(janela_pai, usuario_id, modulo_id)

    for m in modulos:
        ctk.CTkButton(
            janela,
            text=f"{m['nome']}  ({m['total_sinais']} sinais)",
            width=320,
            height=45,
            command=lambda mid=m["id"]: iniciar(mid),
        ).pack(pady=8)


# ---------- lição ----------

def abrir_licao(janela_pai, usuario_id, modulo_id):
    dados = chamar_api("GET", f"/modulos/{modulo_id}/licao", params={"qtd": 5})
    if dados is None:
        return
    questoes = dados["questoes"]

    janela = ctk.CTkToplevel(janela_pai)
    janela.title("Lição")
    janela.geometry("600x760")

    # tudo que muda durante a lição fica neste dicionário
    estado = {
        "indice": 0,
        "acertos": 0,
        "pontos": 0,
        "frames": [],
        "quadro": 0,
        "job": None,
        "botoes": [],
    }

    imagem_vazia = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    vazio = ctk.CTkImage(light_image=imagem_vazia, dark_image=imagem_vazia, size=(1, 1))

    label_titulo = ctk.CTkLabel(janela, text="", font=("Arial", 20, "bold"))
    label_titulo.pack(pady=(20, 5))
    label_enunciado = ctk.CTkLabel(janela, text="", font=("Arial", 18))
    label_enunciado.pack(pady=5)
    label_midia = ctk.CTkLabel(janela, text="")
    label_midia.pack(pady=10)
    frame_opcoes = ctk.CTkFrame(janela, fg_color="transparent")
    frame_opcoes.pack(pady=5)
    label_feedback = ctk.CTkLabel(janela, text="", font=("Arial", 18, "bold"))
    label_feedback.pack(pady=10)
    botao_proximo = ctk.CTkButton(janela, text="Próxima", width=200)

    # ----- animação do GIF -----

    def parar_animacao():
        if estado["job"] is not None:
            try:
                janela.after_cancel(estado["job"])
            except Exception:
                pass
            estado["job"] = None

    def animar(duracao):
        label_midia.configure(image=estado["frames"][estado["quadro"]])
        estado["quadro"] = (estado["quadro"] + 1) % len(estado["frames"])
        if len(estado["frames"]) > 1:
            estado["job"] = janela.after(duracao, animar, duracao)

    def mostrar_midia(arquivo):
        parar_animacao()
        frames, duracao = carregar_frames(arquivo)
        if not frames:
            label_midia.configure(text=f"[mídia não encontrada: {arquivo}]", image=vazio)
            return
        estado["frames"] = frames
        estado["quadro"] = 0
        label_midia.configure(text="")
        animar(duracao)

    def ao_destruir(evento):
        if evento.widget is janela:  # ignora o "destroy" dos widgets filhos
            parar_animacao()

    janela.bind("<Destroy>", ao_destruir)

    # ----- fluxo das questões -----

    def mostrar_questao():
        q = questoes[estado["indice"]]
        label_titulo.configure(text=f"Questão {estado['indice'] + 1} de {len(questoes)}")
        label_enunciado.configure(text=q["enunciado"])
        mostrar_midia(q["midia"])
        label_feedback.configure(text="")
        botao_proximo.pack_forget()

        for widget in frame_opcoes.winfo_children():
            widget.destroy()
        estado["botoes"] = []
        for opcao in q["opcoes"]:
            botao = ctk.CTkButton(
                frame_opcoes,
                text=opcao,
                width=300,
                height=40,
                command=lambda o=opcao: responder(o),
            )
            botao.pack(pady=5)
            estado["botoes"].append(botao)

    def responder(opcao):
        q = questoes[estado["indice"]]
        resultado = chamar_api(
            "POST",
            "/respostas",
            json={
                "usuario_id": usuario_id,
                "sinal_id": q["sinal_id"],
                "resposta": opcao,
            },
        )
        if resultado is None:
            return

        for botao in estado["botoes"]:
            botao.configure(state="disabled")
            if botao.cget("text") == resultado["correta"]:
                botao.configure(fg_color="green")
            elif botao.cget("text") == opcao:
                botao.configure(fg_color="red")

        if resultado["acertou"]:
            estado["acertos"] += 1
            estado["pontos"] += resultado["pontos"]
            label_feedback.configure(
                text=f"Acertou! +{resultado['pontos']} pontos", text_color="lightgreen"
            )
        else:
            label_feedback.configure(
                text=f"Errou. Era: {resultado['correta']}", text_color="salmon"
            )

        ultima = estado["indice"] == len(questoes) - 1
        botao_proximo.configure(text="Finalizar" if ultima else "Próxima")
        botao_proximo.pack(pady=10)

    def proxima():
        estado["indice"] += 1
        if estado["indice"] >= len(questoes):
            finalizar()
        else:
            mostrar_questao()

    def finalizar():
        parar_animacao()
        for widget in janela.winfo_children():
            widget.destroy()
        ctk.CTkLabel(janela, text="Lição concluída!", font=("Arial", 30, "bold")).pack(pady=40)
        ctk.CTkLabel(
            janela,
            text=f"Acertos: {estado['acertos']} de {len(questoes)}\nPontos ganhos: {estado['pontos']}",
            font=("Arial", 22),
        ).pack(pady=20)
        ctk.CTkButton(janela, text="Fechar", width=200, command=janela.destroy).pack(pady=20)

    botao_proximo.configure(command=proxima)
    mostrar_questao()


# ---------- ranking ----------

def abrir_ranking(janela_pai, usuario_id):
    ranking = chamar_api("GET", "/ranking")
    meu = chamar_api("GET", f"/usuarios/{usuario_id}/pontuacao")
    if ranking is None or meu is None:
        return

    janela = ctk.CTkToplevel(janela_pai)
    janela.title("Ranking")
    janela.geometry("520x680")

    ctk.CTkLabel(janela, text="Ranking", font=("Arial", 28, "bold")).pack(pady=15)
    for posicao, linha in enumerate(ranking, start=1):
        ctk.CTkLabel(
            janela,
            text=f"{posicao}º  {linha['usuario']}  -  {linha['pontos']} pts  ({linha['acertos']} acertos)",
            font=("Arial", 16),
        ).pack(pady=3)

    total = meu["total"]
    ctk.CTkLabel(janela, text="Sua pontuação", font=("Arial", 20, "bold")).pack(pady=(25, 5))
    ctk.CTkLabel(
        janela,
        text=f"Total: {total['pontos']} pts  |  {total['acertos']} acertos em {total['respondidas']} respostas",
        font=("Arial", 15),
    ).pack()
    for m in meu["por_modulo"]:
        ctk.CTkLabel(
            janela,
            text=f"{m['modulo']}: {m['pontos']} pts ({m['acertos']}/{m['respondidas']})",
            font=("Arial", 14),
        ).pack(pady=2)

    ctk.CTkButton(janela, text="Fechar", command=janela.destroy).pack(pady=20)
