import socket
import os
from dotenv import load_dotenv
import json

load_dotenv()
HOST = os.getenv('LOCALHOST')
PORT = os.getenv('PORT')

class Client:
    
    def __init__(self) -> None:
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):   
        self.tcp.connect((HOST, int(PORT)))

    def create_msg(self):
        return {}
    
    def send_msg(self):
        self.tcp.send(str.encode(json.dumps(self.create_msg())))
