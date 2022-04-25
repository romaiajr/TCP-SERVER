from ast import Raise
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
            pass
    
    def handle_msg(self, msg: Message):
        event = {"update_list_of_trash": self.update_list_of_trash }
        execute_event = event.get(msg['event'])
        if execute_event:
            execute_event(msg['data'])
    
    def update_list_of_trash(self, data):
        self.list_of_trash = data.get("list_of_trash")
        print(self.list_of_trash)
        time.sleep(1)
    
    def change_list_of_trash(self):
        if self.list_of_trash:
            new_list = {}
            dict_list = self.show_list_of_trash()
            for idx in range(0,len(dict_list)):
                which = input("Selecione o número da lixeira nº {idx}\n".format(idx=idx+1))
                new_list[idx] = self.list_of_trash.get(dict_list[int(which)-1])
            self.list_of_trash = new_list
            print(self.list_of_trash)

    def lock_trash(self):
        print("Lista de lixos: ",self.list_of_trash,self.list_of_trash.keys())
        if self.list_of_trash:
            # print("Lista de lixos preenchidos: ",self.list_of_trash,self.list_of_trash.keys())
            self.show_list_of_trash()
            trash_to_be_locked = input("Qual lixeira deseja travar?\n")
            macs = {id+1:value for id,value in enumerate(self.list_of_trash.keys())}
            print(macs)
            try:
                trash = macs.get(int(trash_to_be_locked))
                self.send_msg(origin="adm",destination="server",mac=self.mac, event="lock_trash",data=trash)
            except Exception as e:
                print(e)
                self.lock_trash()

    def show_list_of_trash(self):
        try:
            idx = 1
            for key in self.list_of_trash.keys():
                print("[{}] - {trash}\n".format(idx, trash=key))
                idx+=1
        except Exception as e:
            print(e)


    def simulate_list_of_trash(self, list_of_trash: list):
        self.list_of_trash = list_of_trash

if __name__ == "__main__":
    import time
    adm = Administrador()
    switchParaPython={
        0:adm.lock_trash(),
    }
    # adm.simulate_list_of_trash({"carro": "Roberto", "moto": "Daniel", "bicicleta": "Samuel"})
    # adm.change_list_of_trash()
    # adm.lock_trash()
    with adm:
        while True:
            adm.await_for_msg()
            time.sleep(1)
            try:
                print(adm.list_of_trash)
                action = input("O que deseja fazer: ")
                if int(action)==0:
                    adm.lock_trash()
                # switchParaPython.get(int(action))
            except:
                print("Valor inválido")