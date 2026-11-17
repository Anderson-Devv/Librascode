import threading

from LibrasCode_Interface_grafica import janela_inicial
from api_librascode import iniciar_api

def rodar_codigo():
    thread_api = threading.Thread(
        target=iniciar_api,
        daemon=True
    )
    thread_api.start()

    janela_inicial.mainloop()

if __name__ == "__main__":
    rodar_codigo()