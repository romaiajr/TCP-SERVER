import json

from message import Message

# Classe para lidar com o envio de mensagens das lixeiras 
class TrashHandler():

    def __init__(self, limit):
        self.lixeiras = {}
        self.lixeiras_connections = {}
        self.limit = limit
        self.msg_dict = {"register": self.connect_trash, "update": self.update_trash, "collect_trash": self.collect_trash}
    
    def handle_msg(self, connection, msg):
        execute = self.msg_dict.get(msg['event'])
        execute(connection=connection, msg=msg)
        reply = str(self.encode_msg(msg))
        connection.send(str.encode(reply))

    def connect_trash(self, connection, msg):
        if len(self.lixeiras_connections) < self.limit:
            mac = msg['mac']
            self.lixeiras[mac] = {"filled_percentage": 0, "isLocked": False}
            self.lixeiras_connections[mac] = connection

    def update_trash(self, msg, **kwargs):
        mac = msg['mac']
        self.lixeiras[mac] = {"filled_percentage": msg['data']['filled_percentage'], "is_locked": msg['data']['is_locked']}

    def get_lixeiras(self):
        return self.lixeiras

    def collect_trash(self, msg, **kwargs):
        mac = msg['data']['mac_to_collect']
        lixeira = self.lixeiras_connections.get(mac)
        if lixeira:
            msg = Message(origin="server",destination="trash",mac=mac, event="collect_trash")
            lixeira.send(json.dumps(msg.get_msg()).encode('utf-8'))

    def encode_msg(self, dict_to_encode):
        return json.dumps(dict_to_encode).encode('utf-8')