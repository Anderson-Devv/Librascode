import socket
import threading
import time

from gerenciamento_dados.api import iniciar_api
from telas.interface import Interface


def api_no_ar():
    try:
        with socket.create_connection(("127.0.0.1", 5000), timeout=0.5):
            return True
    except OSError:
        return False


def esperar_api(limite=10):
    fim = time.time() + limite
    while time.time() < fim:
        if api_no_ar():
            return True
        time.sleep(0.2)
    return False


def main():
    
    if not api_no_ar():
        threading.Thread(target=iniciar_api, daemon=True).start()

    if not esperar_api():
        print("A API não subiu. A porta 5000 está ocupada?")
        return

    app = Interface()
    app.executar()


if __name__ == "__main__":
    main()
