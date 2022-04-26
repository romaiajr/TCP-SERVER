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
            pass
    
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
        
    def collect_trash(self):
        if self.list_to_collect:
            self.send_msg(
                origin="truck",destination="trash",mac=self.mac, event= "collect_trash", 
                data={"mac_to_collect": int(self.list_to_collect[0])})
            self.list_to_collect.pop(0)
#Função chamada quando o arquivo é executado
if __name__ == "__main__":
    import time
    from threading import Thread
    truck = Truck(500)

    def awaitForMessage():
        while True:
            global stop_threads
            truck.await_for_msg()
            time.sleep(1)
            if stop_threads:
                break

    with truck:
        thread = Thread(target=awaitForMessage)
        thread.start()
        stop_threads = False
        while True:
            try:
                print(f"\n\nLixeiras para coleta: \n{truck.list_to_collect}")
                action = int(input("O que deseja fazer: \n1-Coletar primeira lixeira da lista\n2-Atualizar visualmente as lixeiras\n3-Encerrar conexão\n"))
                if action==1:
                    truck.collect_trash()
                elif action==2:
                    continue
                else:
                    stop_threads = True
                    thread.join()
                    break
            except:
                print("Valor inválido")