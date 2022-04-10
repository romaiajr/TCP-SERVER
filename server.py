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
        self.lixeiras_connections = {}
        self.administrador = None
        self.caminhao = None
        self.client_handler = {"lixeira": self.handle_lixeira_msg, "adm": self.handle_adm_msg, "caminhao": self.handle_caminhao_msg}

    def threaded_client(self, connection, client):
        while True:
            msg = connection.recv(2048)
            if msg: 
                print(client, msg)
                res_dict = self.decode_msg(msg)
                handle_msg = self.client_handler[res_dict['client']]
                handle_msg(connection, res_dict)
        
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
        except Exception:
            self.close()
    
    def close(self):
        print("Finalizando conexões")
        if self.lixeiras:
            for lixeira in self.lixeiras:
                lixeira["connection"].close()
        if self.administrador:
            self.administrador.close()
        if self.caminhao:
            self.caminhao.close()
        self.server_socket.close()

    def handle_lixeira_msg(self, connection, msg):
        mac = msg['mac']
        self.lixeiras[mac] = {"filled_percentage": msg["filled_percentage"], "isLocked":msg["isLocked"]}
        self.lixeiras_connections[mac] = {"connection": connection}
        reply = "r" + str(self.encode_msg(msg)) + "b"
        connection.send(str.encode(reply))
        if self.administrador:
            self.administrador.sendall(self.encode_msg(self.lixeiras))
    
    def handle_adm_msg(self, connection, msg):
        self.administrador = connection
        self.administrador.sendall(self.encode_msg(self.lixeiras))
        if msg["to_collect"] and self.caminhao:
            self.caminhao.send(self.encode_msg(msg["to_collect"]))
    
    def handle_caminhao_msg(self, connection, msg):
        self.caminhao = connection
    
    def decode_msg(self, msg):
        return json.loads(msg.decode('utf-8'))
    
    def encode_msg(self, dict_to_encode):
        return json.dumps(dict_to_encode).encode('utf-8')

if __name__ == "__main__":
    server = Server()
    server.run()
