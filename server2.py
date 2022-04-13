import sys
import socket
import selectors
import types
import os
from dotenv import load_dotenv
load_dotenv()
HOST = os.getenv('LOCALHOST')
PORT = os.getenv('PORT')
class Server:

    def __init__(self) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET socket type for IPV4, SOCK_STREAM socket type for server_socket
        self.sel = selectors.DefaultSelector()
    
    def run(self):
        with self.server_socket as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
            server_socket.bind((HOST, int(PORT)))
            server_socket.listen()
            server_socket.setblocking(False) #configure the socket in non-blocking mode
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
    
    def accept_wrapper(self,sock):
        conn, addr = sock.accept()  # Should be ready to read
        print(f"Conexão aceita com o client: {addr}")
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)
    
    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                data.outb += recv_data
                print("Mensagem recebida: {}".format(recv_data))
                self.handle_msg(recv_data)
            else:
                print(f"Encerrando conexão com o cliente: {data.addr}")
                self.sel.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print(f"Enviando mensagem {data.outb!r} to {data.addr}")
                sent = sock.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]
    
    def handle_msg(self, msg):
        pass

if __name__ == "__main__":
    server = Server()
    server.run()