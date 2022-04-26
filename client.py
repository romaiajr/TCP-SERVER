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
#Classe pai de todos os clientes do projeto, adm, lixeira e caminhão herdam essa classe e seus respectivos métodos
class Client:
    #Construtor da classe
    def __init__(self) -> None:
        self.mac = get_mac()
        self.sel = selectors.DefaultSelector()
    #Método chamado no começo do ciclo de vida da instância da  classe
    def __enter__(self):   
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect_ex((HOST, int(PORT)))
        self.client_socket.setblocking(False)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(self.client_socket, events)
        print("Conectado ao servidor")
    #Método chamado no fim do ciclo de vida da instância da  classe
    def __exit__(self,exc_type, exc_value, exc_traceback):
        self.sel.unregister(self.client_socket)
        print("Conexão finalizada")
    #Cria a estrutura da mensagem a ser enviada
    def create_msg(self, origin: str, destination:str, mac:str, event:str, data:dict=None):
        msg = Message(origin, destination, mac, event, data)
        return msg.get_msg()
    #Envia uma mensagem criada anteriormente
    def send_msg(self, origin: str, destination:str, mac:str, event:str, data:dict=None):
        msg = self.create_msg(origin, destination, mac, event, data)
        print("Enviando mensagem: {}".format(msg))
        self.client_socket.send(str.encode(json.dumps(msg)))
    #Receber quantidae de bytes como mensagem
    def recv_msg(self):
        return self.client_socket.recv(1024)
    #Método para converter String->JSON
    def decode_msg(self, msg):
        return json.loads(msg)
