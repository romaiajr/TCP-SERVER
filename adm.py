from client import Client
from message import Message
import time

class Administrador(Client):

    def __init__(self) -> None:
        super().__init__()
        self.list_of_trash = {}
    
    def __enter__(self):
        super().__enter__()
        self.send_msg(origin="adm",destination="server",mac=self.mac, event="register")
    
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
        event = {"update_list_of_trash": self.update_list_of_trash }
        execute_event = event.get(msg['event'])
        if execute_event:
            execute_event(msg['data'])
    
    def update_list_of_trash(self, data):
        if data.get('list_of_trash'):
            list_of_trash = data.get('list_of_trash')
        elif data.get('mac'):
            list_of_trash.append(data.get('mac'))
        print(list_of_trash)
        time.sleep(1)
    
    def change_list_of_trash(self):
        new_list = {}
        dict_list = self.show_list_of_trash()
        for idx in range(0,len(dict_list)):
            which = input("Selecione o número da lixeira nº {idx}\n".format(idx=idx+1))
            new_list[idx] = self.list_of_trash.get(dict_list[int(which)-1])
        self.list_of_trash = new_list
        print(self.list_of_trash)

    def lock_trash(self):
        dict_list = self.show_list_of_trash()
        which = input("Qual lixeira deseja travar?\n")
        print(self.list_of_trash.get(dict_list[int(which)-1]))

    def show_list_of_trash(self):
        idx = 1
        for key in self.list_of_trash.keys():
            print("[{}] - {trash}\n".format(idx, trash={self.list_of_trash.get(key)}))
            idx+=1
        return list(self.list_of_trash)

    def simulate_list_of_trash(self, list_of_trash: list):
        self.list_of_trash = list_of_trash

if __name__ == "__main__":
    import time
    adm = Administrador()
    adm.simulate_list_of_trash({"carro": "Roberto", "moto": "Daniel", "bicicleta": "Samuel"})
    adm.change_list_of_trash()
    adm.lock_trash()
    # with truck:
    #     while True:
    #         truck.await_for_msg()
    #         time.sleep(1)