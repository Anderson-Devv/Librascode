import os
import random
from flask import Flask, jsonify, request, send_from_directory
from gerenciamento_dados.librascodebd import conexao_banco

app = Flask(__name__)


RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_MIDIA = os.path.join(RAIZ, "files", "midia")
PASTA_STICKERS = os.path.join(RAIZ, "files", "stickers")
PASTA_GUIAS = os.path.join(RAIZ, "files", "guias")
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

# ---------- ranking ----------

@app.get("/ranking")
def ranking():
    linhas = consultar(
        """
        SELECT c.idcadastrolibrascode AS usuario_id,
               c.usuario AS usuario,
               COALESCE(SUM(r.acertou), 0) AS acertos,
               COALESCE(SUM(r.pontos), 0) AS pontos,
               DENSE_RANK() OVER (ORDER BY COALESCE(SUM(r.pontos), 0) DESC) AS ranking
        FROM cadastrolibrascode c
        LEFT JOIN respostas r ON r.usuario_id = c.idcadastrolibrascode
        GROUP BY c.idcadastrolibrascode, c.usuario
        ORDER BY ranking, c.usuario
        """
    )
    for linha in linhas:
        linha["acertos"] = int(linha["acertos"])
        linha["pontos"] = int(linha["pontos"])
    return jsonify(linhas)
    
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

# ---------- Guia inicial ----------

@app.get("/guia")
def baixar_guia():

    return send_from_directory(
        PASTA_GUIAS,
        "guia_licoes.pdf",
        as_attachment=True
    )

# ---------- Pesquisa e Favoritar----------

@app.get("/pesquisa")
def buscar_itens():
    
    termo = request.args.get("termo", "")
    
    pesquisa = consultar(
        """
        SELECT id, palavra, midia
        FROM sinais
        WHERE palavra LIKE %s
        ORDER BY palavra ASC
        """,
        (f"%{termo}%",)
    )
    return jsonify(pesquisa)

@app.get("/modulos/<int:modulo_id>/licao")
def gerar_licao(modulo_id):
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
            }
        )
    return jsonify({"modulo_id": modulo_id, "questoes": questoes})

@app.post("/favoritos")
def favoritar():

    dados = request.get_json()

    usuario_id = dados.get("usuario_id")
    sinal_id = dados.get("sinal_id")

    ja_existe = consultar(
            """
            SELECT id
            FROM favoritos
            WHERE usuario_id = %s
            AND sinal_id = %s
            """,
        (usuario_id, sinal_id),
        um=True
    )

    if ja_existe:
        return jsonify({
            "mensagem": "Já favoritado."
        })
    executar(
        """
            INSERT INTO favoritos
            (usuario_id, sinal_id)
            VALUES (%s, %s)
            """,
        (usuario_id, sinal_id)
    )

    return jsonify({
        "mensagem": "Favorito adicionado!"
    })
    
@app.get("/favoritos/<int:usuario_id>")
def listar_favoritos(usuario_id):

    favoritos = consultar(
        """
        SELECT
            s.id,
            s.palavra,
            s.midia
        FROM favoritos f
        INNER JOIN sinais s
            ON s.id = f.sinal_id
        WHERE f.usuario_id = %s
        """,
        (usuario_id,)
    )

    return jsonify(favoritos)

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
    
    verificar_conquistas(usuario_id)
    
    return jsonify({"acertou": acertou, "correta": sinal["palavra"], "pontos": pontos})

# ---------- conquistas e certificado ----------
def verificar_conquistas(usuario_id):
    total_pontos = consultar(
        """
        SELECT COALESCE(SUM(pontos),0) AS total
        FROM respostas
        WHERE usuario_id = %s
        """,
        (usuario_id,),
        um=True
    )
    pontos = total_pontos["total"]

    conquistas = consultar(
        """
        SELECT *
        FROM conquistas
        WHERE pontos_necessarios <= %s
        """,
        (pontos,)
    )

    for conquista in conquistas:
        existe = consultar(
            """
            SELECT id
            FROM usuario_conquistas
            WHERE usuario_id = %s
            AND conquista_id = %s
            """,
            (usuario_id, conquista["id"]),
            um=True
        )

        if not existe:

            executar(
                """
                INSERT INTO usuario_conquistas
                (usuario_id, conquista_id)
                VALUES (%s,%s)
                """,
                (usuario_id, conquista["id"])
            )
    return pontos
    
@app.get("/conquistas/<int:usuario_id>")
def listar_conquistas(usuario_id):

    conquistas = consultar(
        """
        SELECT
            c.nome,
            c.descricao,
            c.sticker,
            c.pontos_necessarios
            FROM conquistas c
            INNER JOIN usuario_conquistas uc
                ON uc.conquista_id = c.id
            WHERE uc.usuario_id = %s
            ORDER BY c.pontos_necessarios
        """,
        (usuario_id,)
    )

    return jsonify(conquistas)

def verificar_certificado(usuario_id):

    resultado_modulos = consultar(
        """
        SELECT COUNT(*) AS total
        FROM modulos
        """,
        um=True
    )
    total_modulos = resultado_modulos["total"]

    resultado_concluidos = consultar(
        """
        SELECT COUNT(DISTINCT modulo_id) AS total
        FROM historico_modulo
        WHERE usuario_id = %s
        """,
        (usuario_id,),
        um=True
    )
    concluidos = resultado_concluidos["total"]

    return concluidos >= total_modulos

@app.get("/stickers/<path:arquivo>")
def servir_sticker(arquivo):
    return send_from_directory(PASTA_STICKERS, arquivo)

# ---------- histórico de lições ----------

@app.post("/historico")
def registrar_historico():
    
    ja_existe = consultar(
        """
        SELECT id
        FROM historico_modulo
        WHERE usuario_id = %s
        AND modulo_id = %s
        """,
        (usuario_id, modulo_id),
        um=True
    )

    if ja_existe:
        return jsonify({
            "mensagem": "Módulo já registrado."
        }), 200

    dados = request.get_json(silent=True) or {}

    usuario_id = dados.get("usuario_id")
    modulo_id = dados.get("modulo_id")
    pontuacao = dados.get("pontuacao")

    if usuario_id is None or modulo_id is None or pontuacao is None:
        return erro("Envie usuario_id, modulo_id e pontuacao.")

    try:
        usuario_id = int(usuario_id)
        modulo_id = int(modulo_id)
        pontuacao = int(pontuacao)
    except (ValueError, TypeError):
        return erro("Os identificadores e a pontuação devem ser números.")

    if usuario_id <= 0 or modulo_id <= 0 or pontuacao < 0:
        return erro("Valores inválidos.")

    usuario = consultar(
        "SELECT idcadastrolibrascode FROM cadastrolibrascode WHERE idcadastrolibrascode = %s",
        (usuario_id,),
        um=True
    )

    if not usuario:
        return erro("Usuário não encontrado.", 404)

    modulo = consultar(
        "SELECT id FROM modulos WHERE id = %s",
        (modulo_id,),
        um=True
    )

    if not modulo:
        return erro("Módulo não encontrado.", 404)

    novo_id = executar(
        """
        INSERT INTO historico_modulo
        (usuario_id, modulo_id, pontuacao)
        VALUES (%s, %s, %s)
        """,
        (usuario_id, modulo_id, pontuacao)
    )

    return jsonify({
        "mensagem": "Realização registrada com sucesso!",
        "historico_id": novo_id,
        "pontuacao": pontuacao
    }), 201

# ---------- mídia ----------

@app.get("/midia/<path:arquivo>")
def servir_midia(arquivo):
    return send_from_directory(PASTA_MIDIA, arquivo)


def iniciar_api():
    os.makedirs(PASTA_MIDIA, exist_ok=True)
    os.makedirs(PASTA_STICKERS,exist_ok=True)
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    iniciar_api()
