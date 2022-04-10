import json
import socket
import os
from dotenv import load_dotenv
from _thread import *

load_dotenv()
HOST = os.getenv('LOCALHOST')
PORT = os.getenv('PORT')

class Server:

    def __init__(self) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET socket type for IPV4, SOCK_STREAM socket type for server_socket
        self.lixeiras = {}

    def threaded_client(self, connection, client):
        msg = connection.recv(2048)
        if msg: 
            self.verify_client(msg)
            reply = "r" + msg.decode('utf-8') + "b"
            print(client, msg)
            connection.sendall(str.encode(reply))
        print('Finalizando conexao do cliente: {}'.format(client))
        connection.close()
        
    def run(self):
        try:
            with self.server_socket as server_socket:
                server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
                server_socket.bind((HOST, int(PORT)))
                server_socket.listen()
                print(f"Servidor Online, escutando a porta {PORT}")
                while True:
                    connection, client = server_socket.accept()
                    print(f"Conexão estabelecida com o cliente: {client}")
                    start_new_thread(self.threaded_client,(connection, client))
        except Exception as e:
            print(e)
            server_socket.close()

    def verify_client(self, msg):
        res_dict = json.loads(msg.decode('utf-8'))
        if res_dict['client'] == 'lixeira':
            self.update_lixeira(res_dict)

    def update_lixeira(self, msg):
        mac = msg['mac']
        self.lixeiras[mac] = {"filled_percentage": msg["filled_percentage"], "isLocked":msg["isLocked"]}

if __name__ == "__main__":
    server = Server()
    server.run() 