import LibrasCode_Interface_grafica
from api_librascode import iniciar_api
import threading
import time


def main():
   
      thread_api = threading.Thread(target=iniciar_api, daemon=True)
      thread_api.start()
      time.sleep(1)
      LibrasCode_Interface_grafica.janela_inicial.mainloop()
      
if __name__ == "__main__":
   main()   