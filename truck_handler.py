import json
from message import Message

# Classe para lidar com o envio de mensagens dos caminhões 
class TruckHandler():

    def __init__(self, limit):
        self.truck = None
        self.limit = limit
        self.msg_dict = {"register": self.register, "update_list_to_collect": self.update_list_to_collect}
    
    def handle_msg(self, connection, msg):
        execute = self.msg_dict.get(msg['event'])
        execute(connection=connection, msg=msg)

    def register(self, connection, **kwargs):
        self.truck = connection
    
    def is_connected(self):
        return self.truck
    
    def update_list_to_collect(self, mac: str, **kwargs):
        msg = Message(origin="server",destination="truck",mac=None, event="update_list_to_collect", data={ 'mac': mac })
        self.truck.send(json.dumps(msg.get_msg()).encode('utf-8'))
    
    def get_list_to_collect(self):
        return self.list_to_collect

    def encode_msg(self, dict_to_encode):
        return json.dumps(dict_to_encode).encode('utf-8')