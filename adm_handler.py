import json

# Classe para lidar com o envio de mensagens das lixeiras 
class AdmHandler():

    def __init__(self, limit):
        self.administrador = None
        self.limit = limit
        self.msg_dict = {"connect": self.connect, "send_to_collect": self.send_to_collect}
    
    def handle_msg(self, connection, msg):
        execute = self.msg_dict.get(msg['type'])
        execute(connection=connection, msg=msg)
        reply = str(self.encode_msg(msg))
        connection.send(str.encode(reply))

    def connect(self, connection, **kwargs):
        self.administrador = connection
    
    def is_connected(self):
        return self.administrador
    
    def send_to_collect(self, msg, **kwargs):
        if msg["to_collect"]:
            print(msg["to_collect"])
            # self.caminhao.send(self.encode_msg(msg["to_collect"]))
    
    def send_msg(self, msg):
        self.administrador.sendall(self.encode_msg(msg))

    def encode_msg(self, dict_to_encode):
        return json.dumps(dict_to_encode).encode('utf-8')