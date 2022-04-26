from concurrent.futures import thread
from client import Client
from message import Message

class Lixeira(Client):

    def __init__(self, capacity: int) -> None:
        super().__init__()
        self.capacity = capacity
        self.filled = 0
        self.is_locked = False
    
    def __enter__(self):
        super().__enter__()
        self.send_msg(origin="trash",destination="server",mac=self.mac, event="register")
    
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
        event = {"lock_trash": self.lock, "unlock_trash": self.unlock, "collect_trash": self.empty }
        execute_event = event.get(msg['event'])
        if execute_event:
            execute_event()
            self.send_msg(
                origin="trash",destination="server",mac=self.mac, event="update", 
                data={'filled_percentage': self.filled_percentage(), "is_locked": self.is_locked })

    def fill(self, value: int):
        if self.is_locked:
            return
        elif value <= self.capacity - self.filled:
            self.filled += value
            if self.filled == self.capacity:
                self.lock()
        else:
            self.lock()
        self.send_msg(
            origin="trash",destination="server",mac=self.mac, event="update", 
            data={'filled_percentage': self.filled_percentage(), "is_locked": self.is_locked })
        
    def empty(self):
        self.filled = 0
        self.unlock()
        print("Lixeira Coletada!")
        
    def lock(self):
        self.is_locked = True
        
    def unlock(self):
        self.is_locked = False

    def filled_percentage(self) -> float:
        return (self.filled * 100)/self.capacity
#Função chamada quando o arquivo é executado
if __name__ == "__main__":
    import time
    from threading import Thread
    lixeira = Lixeira(500)
    def awaitForMessage():
        while True:
            global stop_threads
            lixeira.await_for_msg()
            time.sleep(1)
            if stop_threads:
                break
            
    with lixeira:
        thread = Thread(target=awaitForMessage)
        thread.start()
        stop_threads = False
        while True:
            try:
                print("\n\nEstado da lixeira:\nCapacidade Ocupada da lixeira/Porcentagem de ocupação: ",lixeira.filled,"/",lixeira.capacity,"(",lixeira.filled_percentage(),"%)","Estado de abertura: ",not lixeira.is_locked)
                action = int(input("\n\nO que deseja fazer: \n1-Inserir Lixo\n2-Atualizar visualmente a lixeira\n3-Encerrar conexão\n"))
                if action==1:
                    quantidadeLixo = int(input(
                        "Deseja inserir quantas unidades de lixo?"))
                    if not lixeira.is_locked:
                        lixeira.fill(quantidadeLixo)
                        print(f"Capacidade atual: {lixeira.filled_percentage()}%")
                    else:
                        print("Lixeira está fechada!")
                elif action==2:
                    continue
                else:
                    stop_threads = True
                    thread.join()
                    break
            except:
                print("Valor inválido")