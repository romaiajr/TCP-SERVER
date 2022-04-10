import json

# Classe para lidar com o envio de mensagens das lixeiras 
class TrashHandler():

    def __init__(self, limit):
        self.lixeiras = {}
        self.lixeiras_connections = {}
        self.limit = limit
        self.msg_dict = {"connect": self.connect_trash, "fill": self.fill_trash}
    
    def handle_msg(self, connection, msg):
        execute = self.msg_dict.get(msg['type'])
        execute(connection=connection, msg=msg)
        reply = str(self.encode_msg(msg))
        connection.send(str.encode(reply))

    def connect_trash(self, connection, msg):
        if len(self.lixeiras_connections) < self.limit:
            mac = msg['mac']
            self.lixeiras[mac] = {"filled_percentage": 0, "isLocked": False}
            self.lixeiras_connections[mac] = {"connection": connection}

    def fill_trash(self, msg, **kwargs):
        mac = msg['mac']
        self.lixeiras[mac] = {"filled_percentage": msg['filled_percentage'], "isLocked": msg['isLocked']}

    def get_lixeiras(self):
        return self.lixeiras
    
    def encode_msg(self, dict_to_encode):
        return json.dumps(dict_to_encode).encode('utf-8')