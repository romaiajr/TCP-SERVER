from client import Client
from message import Message
import time

class Truck(Client):

    def __init__(self, capacity: int) -> None:
        super().__init__()
        self.capacity = capacity
        self.filled = 0
        self.list_to_collect = []
    
    def __enter__(self):
        super().__enter__()
        self.send_msg(origin="truck",destination="server",mac=self.mac, event="register")
    
    def await_for_msg(self):
        try:
            msg = self.recv_msg()
            if msg:
                msg_decoded = self.decode_msg(msg)
                print("Mensagem recebida: {}".format(msg_decoded))
                self.handle_msg(msg_decoded)
        except Exception as e:
            print(e)
    
    def handle_msg(self, msg: Message):
        event = {"update_list_to_collect": self.update_list_to_collect }
        execute_event = event.get(msg['event'])
        if execute_event:
            execute_event(msg['data'])
    
    def update_list_to_collect(self, data):
        if data.get('list_to_collect'):
            self.list_to_collect = data.get('list_to_collect')
        elif data.get('mac'):
            self.list_to_collect.append(data.get('mac'))
        print(self.list_to_collect)
        time.sleep(1)
        self.collect_trash()
        
    def collect_trash(self):
        for trash in self.list_to_collect:
            self.send_msg(
                origin="truck",destination="trash",mac=self.mac, event= "collect_trash", 
                data={"mac_to_collect": trash})
            time.sleep(1)
        self.list_to_collect = []

if __name__ == "__main__":
    import time
    truck = Truck(500)
    with truck:
        while True:
            truck.await_for_msg()
            time.sleep(1)