"""
Framework do cadastrolibrascode (Flask).

Rodar:  python api_cadastrolibrascode.py   (deixe rodando em um terminal)
Depende de: pip install flask mysql-connector-python

Rotas:
  GET  /modulos                      lista os módulos
  GET  /modulos/<id>/licao?qtd=5     GERA uma lição (questões aleatórias, sem o gabarito)
  POST /respostas                    corrige a resposta, guarda e devolve os pontos
  GET  /ranking                      top 10 usuários por pontuação
  GET  /usuarios/<id>/pontuacao      pontuação total e por módulo de um usuário
  POST /sinais                       cadastra um novo sinal (palavra + arquivo de mídia)
  GET  /midia/<arquivo>              serve imagens/gifs da pasta ./midia
"""
import os
import random

from flask import Flask, jsonify, request, send_from_directory

from librascodebd import conexao_banco

app = Flask(__name__)

PASTA_MIDIA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "midia")
PONTOS_POR_ACERTO = 10
QTD_PADRAO = 5


# ---------- acesso ao banco ----------

def consultar(sql, params=(), um=False):
    conexao = conexao_banco()
    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(sql, params)
        dados = cursor.fetchone() if um else cursor.fetchall()
        cursor.close()
        return dados
    finally:
        conexao.close()


def executar(sql, params=()):
    conexao = conexao_banco()
    try:
        cursor = conexao.cursor()
        cursor.execute(sql, params)
        conexao.commit()
        novo_id = cursor.lastrowid
        cursor.close()
        return novo_id
    finally:
        conexao.close()


def erro(mensagem, codigo=400):
    return jsonify({"erro": mensagem}), codigo


# ---------- módulos e lições ----------

@app.get("/modulos")
def listar_modulos():
    modulos = consultar(
        """
        SELECT m.id, m.nome, m.descricao, COUNT(s.id) AS total_sinais
        FROM modulos m
        LEFT JOIN sinais s ON s.modulo_id = m.id
        GROUP BY m.id, m.nome, m.descricao, m.ordem
        ORDER BY m.ordem
        """
    )
    return jsonify(modulos)


@app.get("/modulos/<int:modulo_id>/licao")
def gerar_licao(modulo_id):
    """Cria as questões na hora: 'Que palavra representa este sinal?'
    A resposta certa é a palavra do sinal; as erradas vêm de outros sinais."""
    sinais = consultar(
        "SELECT id, palavra, midia FROM sinais WHERE modulo_id = %s", (modulo_id,)
    )
    if not sinais:
        return erro("Módulo não encontrado ou sem sinais cadastrados.", 404)

    todas_palavras = {s["palavra"] for s in consultar("SELECT palavra FROM sinais")}
    if len(todas_palavras) < 2:
        return erro("Cadastre pelo menos 2 sinais para gerar questões.", 400)

    qtd = request.args.get("qtd", QTD_PADRAO, type=int)
    qtd = max(1, min(qtd, len(sinais)))

    questoes = []
    for sinal in random.sample(sinais, qtd):
        erradas = list(todas_palavras - {sinal["palavra"]})
        opcoes = random.sample(erradas, min(3, len(erradas))) + [sinal["palavra"]]
        random.shuffle(opcoes)
        questoes.append(
            {
                "sinal_id": sinal["id"],
                "enunciado": "Que palavra este sinal representa?",
                "midia": sinal["midia"],
                "opcoes": opcoes,
                # o gabarito NÃO é enviado aqui; ele só aparece depois da resposta
            }
        )
    return jsonify({"modulo_id": modulo_id, "questoes": questoes})


# ---------- respostas e pontuação ----------

@app.post("/respostas")
def responder():
    dados = request.get_json(silent=True) or {}
    usuario_id = dados.get("usuario_id")
    sinal_id = dados.get("sinal_id")
    resposta = dados.get("resposta")

    if not usuario_id or not sinal_id or not resposta:
        return erro("Envie usuario_id, sinal_id e resposta.")

    sinal = consultar("SELECT palavra FROM sinais WHERE id = %s", (sinal_id,), um=True)
    if not sinal:
        return erro("Sinal não encontrado.", 404)

    usuario = consultar(
        "SELECT idcadastrolibrascode FROM cadastrolibrascode WHERE idcadastrolibrascode = %s",
        (usuario_id,),
        um=True,
    )
    if not usuario:
        return erro("Usuário não encontrado.", 404)

    acertou = resposta == sinal["palavra"]
    pontos = PONTOS_POR_ACERTO if acertou else 0

    executar(
        "INSERT INTO respostas (usuario_id, sinal_id, acertou, pontos) VALUES (%s, %s, %s, %s)",
        (usuario_id, sinal_id, int(acertou), pontos),
    )
    return jsonify({"acertou": acertou, "correta": sinal["palavra"], "pontos": pontos})


# ---------- conteúdo (cadastro de sinais) e mídia ----------

@app.post("/sinais")
def criar_sinal():
    dados = request.get_json(silent=True) or {}
    modulo_id = dados.get("modulo_id")
    palavra = (dados.get("palavra") or "").strip()
    midia = (dados.get("midia") or "").strip()

    if not modulo_id or not palavra or not midia:
        return erro("Envie modulo_id, palavra e midia.")
    if not os.path.exists(os.path.join(PASTA_MIDIA, midia)):
        return erro(f"Arquivo '{midia}' não existe na pasta midia/.", 404)

    novo_id = executar(
        "INSERT INTO sinais (modulo_id, palavra, midia) VALUES (%s, %s, %s)",
        (modulo_id, palavra, midia),
    )
    return jsonify({"id": novo_id, "palavra": palavra, "midia": midia}), 201


@app.get("/midia/<path:arquivo>")
def servir_midia(arquivo):
    return send_from_directory(PASTA_MIDIA, arquivo)


def iniciar_api():
    os.makedirs(PASTA_MIDIA, exist_ok=True)
    # debug e reloader desligados: eles não funcionam fora da thread principal
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)


if __name__ == "__main__":
    iniciar_api()