
import requests


class APICliente:

    def __init__(self):
        self.api = "http://127.0.0.1:5000"

    def chamar(self, metodo, rota, **kwargs):

        try:
            resposta = requests.request(
                metodo,
                self.api + rota,
                timeout=5,
                **kwargs
            )

            resposta.raise_for_status()

            return resposta.json()

        except requests.RequestException as erro:
            print(f"Erro ao conectar com a API: {erro}")
            return None
