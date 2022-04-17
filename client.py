import socket
import os
import selectors
import json
from uuid import getnode as get_mac
from message import Message
from dotenv import load_dotenv
load_dotenv()
HOST = os.getenv('LOCALHOST')
PORT = os.getenv('PORT')

class Client:
    
    def __init__(self) -> None:
        self.mac = get_mac()
        self.sel = selectors.DefaultSelector()

    def __enter__(self):   
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect_ex((HOST, int(PORT)))
        self.client_socket.setblocking(False)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(self.client_socket, events)
        print("Conectado ao servidor")

    def __exit__(self,exc_type, exc_value, exc_traceback):
        self.sel.unregister(self.client_socket)
        print("Conexão finalizada")
        
    def create_msg(self, origin: str, destination:str, mac:str, event:str, data:dict=None):
        msg = Message(origin, destination, mac, event, data)
        return msg.get_msg()
    
    def send_msg(self, origin: str, destination:str, mac:str, event:str, data:dict=None):
        msg = self.create_msg(origin, destination, mac, event, data)
        print("Enviado mensagem: {}".format(msg))
        self.client_socket.send(str.encode(json.dumps(msg)))
    
    def recv_msg(self):
        return self.client_socket.recv(1024)
    
    def decode_msg(self, msg):
        print(msg)
        return json.loads(msg)
