import json
import socket
import os
from dotenv import load_dotenv
from _thread import *
from adm_handler import AdmHandler
from lixeira_handler import TrashHandler
from truck_handler import TruckHandler
load_dotenv()
HOST = os.getenv('LOCALHOST')
PORT = os.getenv('PORT')

class Server:

    def __init__(self) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET socket type for IPV4, SOCK_STREAM socket type for server_socket
        self.trash_handler = TrashHandler(5)
        self.adm_handler = AdmHandler(1)
        self.truck_handler = TruckHandler(1)
        self.client_handler = {"trash": self.handle_lixeira_msg, "adm": self.handle_adm_msg, "truck": self.handle_truck_msg}

    def threaded_client(self, connection, client):
        while True:
            msg = connection.recv(2048)
            if msg: 
                print(client, msg)
                res_dict = self.decode_msg(msg)
                handle_msg = self.client_handler[res_dict['origin']]
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
        except KeyboardInterrupt:
            print("Finalizando servidor")
            self.server_socket.close()

    #TODO alterar a lógica dos handlers
    def handle_lixeira_msg(self, connection, msg):
        self.trash_handler.handle_msg(connection, msg)
        if msg['event'] == "update":
            if float(msg['data']['filled_percentage']) > 80:
                if self.truck_handler.is_connected():
                    self.truck_handler.update_list_to_collect(msg['mac'])
    
    def handle_truck_msg(self, connection, msg):
        if msg['event'] == 'collect_trash':
            self.trash_handler.handle_msg(connection, msg)
        else: 
            self.truck_handler.handle_msg(connection, msg)
    
    def handle_adm_msg(self, connection, msg):
        self.adm_handler.handle_msg(connection, msg)
        self.adm_handler.send_msg((self.trash_handler.get_lixeiras()))
        # if self.caminhao:
        #     self.caminhao.send(self.encode_msg(msg["to_collect"]))
    
    def decode_msg(self, msg):
        return json.loads(msg.decode('utf-8'))

if __name__ == "__main__":
    server = Server()
    server.run()