import socket
import os
from dotenv import load_dotenv
import json
from uuid import getnode as get_mac

load_dotenv()
HOST = os.getenv('LOCALHOST')
PORT = os.getenv('PORT')

class Client:
    
    def __init__(self) -> None:
        self.mac = get_mac()

    def __enter__(self):   
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST, int(PORT)))
        print("Conectado ao servidor")

    def __exit__(self,exc_type, exc_value, exc_traceback):
        self.client_socket.close()
        print("Conexão finalizada")
        
    def create_msg(self):
        return {}
    
    def send_msg(self):
        print("Enviado mensagem: {}".format(self.create_msg()))
        self.client_socket.send(str.encode(json.dumps(self.create_msg())))
    
    def recv_msg(self):
        return self.client_socket.recv(1024)
