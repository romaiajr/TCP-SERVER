import json
import sys
import socket
import selectors
import types
import os
from dotenv import load_dotenv
from message_handler import MessageHandler

load_dotenv()
HOST = os.getenv('LOCALHOST')
PORT = os.getenv('PORT')
#Classe responsável pelo servidor
class Server:
    #Construtor da classe 
    def __init__(self) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET socket type for IPV4, SOCK_STREAM socket type for server_socket
        self.sel = selectors.DefaultSelector()#Atributo responsável pelo multi-thread
        self.handler = MessageHandler(1,5,1)
    
    def run(self):
        with self.server_socket as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#Configuração do socket
            server_socket.bind((HOST, int(PORT)))#Estabelecendo o host e a porta
            server_socket.listen()#Escutando mensagens recebidas
            server_socket.setblocking(False) #Permite que mais de uma conexão ocorra no socket
            self.sel.register(server_socket, selectors.EVENT_READ, data=None)
            print(f"Servidor Online, escutando a porta {PORT}")
            try:
                while True:
                    events = self.sel.select(timeout=None)
                    for key, mask in events:
                        if key.data is None:
                            self.accept_wrapper(key.fileobj)
                        else:
                            self.service_connection(key, mask)
            except KeyboardInterrupt:
                print("Caught keyboard interrupt, exiting")
            finally:
                self.sel.close()
    #Método responsável pelo registro dos clientes com uma thread específica
    def accept_wrapper(self,sock):
        conn, addr = sock.accept()  # Should be ready to read
        print(f"Conexão aceita com o client: {addr}")
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)
    #Lidar com os dados que chegam das mensagens
    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                data.outb += recv_data
                print("Mensagem recebida: {}".format(recv_data))
                self.handler.handle_msg(self.decode_msg(recv_data), sock)
            else:
                print(f"Encerrando conexão com o cliente: {data.addr}")
                self.sel.unregister(sock)
                sock.close()

    def decode_msg(self, msg):
        return json.loads(msg)
#Função chamada quando o arquivo é executado
if __name__ == "__main__":
    server = Server()
    server.run()