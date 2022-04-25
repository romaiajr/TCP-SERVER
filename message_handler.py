from message import Message
import json
from uuid import getnode as get_mac

class MessageHandler:

    def __init__(self, truck_limit, trash_limit, adm_limit):
        self.mac = get_mac()
        self.truck = None
        self.adm = None
        self.trash_connections = {}
        self.trash = {}
        self.to_collect = []
        self.truck_limit = truck_limit
        self.trash_limit = trash_limit
        self.adm_limit = adm_limit
    
    def handle_msg(self, msg, connection):
        if msg['event'] == "register":
            self.register_client(msg, connection)
        elif msg['event'] == "update":
            self.update_trash(msg, connection)
            if self.adm:
                self.adm.send("messagem da atualização")
        elif msg['event'] == "collect_trash":
            self.collect_trash(msg, connection)
        
    def register_client(self, msg, connection):
        if msg['origin'] == "trash":
            if len(self.trash_connections) < self.trash_limit:
                mac = msg['mac']
                self.trash[mac] = {"filled_percentage": 0, "isLocked": False}
                self.trash_connections[mac] = connection
                print(self.adm)
                if self.adm:
                    msg_to_adm = Message(origin="server", destination="adm", mac=self.mac, event="update_list_of_trash", data={"list_of_trash": self.trash})
                    print(self.adm)
                    self.send(self.adm, msg_to_adm)
        elif not self.truck and msg['origin'] == 'truck':
            self.truck = connection
            msg_to_truck = Message(origin="server",destination="truck",mac=self.mac, event="update_list_to_collect", data={"list_to_collect": self.to_collect})
            self.send_msg(self.truck, msg_to_truck)
        elif not self.adm and msg['origin'] == 'adm':
            self.adm = connection
            msg_to_adm = Message(origin="server", destination="adm", mac=self.mac, event="update_list_of_trash", data={"list_of_trash": self.trash})
            self.send_msg(connection, msg_to_adm)
    
    def update_trash(self, msg, connection):
        filled_percentage = float(msg['data']['filled_percentage'])
        is_locked = msg['data']['is_locked']
        mac = msg['mac']
        self.trash[mac] = {"filled_percentage": filled_percentage, "is_locked": is_locked}
        if filled_percentage >= 85 or is_locked:
            if mac not in self.to_collect:
                self.to_collect.append(mac)
                print("Lixeiras prontas para coleta: {}".format(self.to_collect))
                if self.truck:
                    msg = Message(origin="server",destination="truck",mac=self.mac, event="update_list_to_collect", data={"list_to_collect": self.to_collect})
                    self.send_msg(self.truck, msg)
        print("Vai entrar?")
        if self.adm:
            print("Entrei")
            msg_to_adm = Message(origin="server", destination="adm", mac=self.mac, event="update_list_of_trash", data={"list_of_trash": self.trash})
            self.send(self.adm, msg_to_adm)

    def collect_trash(self, msg, connection):
        mac = msg['data']['mac_to_collect']
        lixeira = self.trash_connections.get(mac)
        if lixeira:
            msg = Message(origin="server",destination="trash",mac=self.mac, event="collect_trash")
            self.send_msg(lixeira, msg)
            self.to_collect.remove(mac)
    
    def send_msg(self, destination, msg):
        sent = json.dumps(msg.get_msg()).encode('utf-8')
        print(f"Enviando mensagem {sent}")
        destination.send(sent)