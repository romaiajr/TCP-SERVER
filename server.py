import socket
import os
from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv('LOCALHOST')
PORT = os.getenv('PORT')

class Server:

    def __init__(self) -> None:
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET IPV4, SOCK_STREAM socket type for tcp

    def run(self):
        try:
            with self.tcp as tcp:
                tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                tcp.bind((HOST, int(PORT)))
                tcp.listen()
                print(f"Servidor Online, escutando a porta {PORT}")
                while True:
                    connection, client = tcp.accept()
                    print(f"Conexão estabelecida com o cliente: {client}")
                    while True:
                        msg = connection.recv(1024)
                        if not msg: break
                        print(client, msg)
                    print('Finalizando conexao do cliente')
                    connection.close()
        except KeyboardInterrupt:
            print('interrupted!')
   
if __name__ == "__main__":
    server = Server()
    server.run() 