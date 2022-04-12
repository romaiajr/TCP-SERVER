from client import Client
from message import Message

class Lixeira(Client):

    def __init__(self, capacity: int) -> None:
        super().__init__()
        self.capacity = capacity
        self.filled = 0
        self.is_locked = False
        self.send_msg(origin="lixeira",destination="server",event="register")
    
    #REVIEW a forma de iniciar o client a ponto dele receber msg e ser preenchido
    #REVIEW talvez coroutine para verificar em loop sem atrapalhar o fluxo do código
    #TODO rever as mensagens exibidas nos prints
    def await_for_msg(self):
        try:
            msg = self.recv_msg()
            if msg:
                print("Mensagem recebida: {}".format(msg))
                self.handle_msg(msg)
        except Exception as e:
            print(e)
    
    def handle_msg(self, msg: Message):
        event = {"lock_trash": self.lock, "unlock_trash": self.unlock, "collect_trash": self.empty }
        execute_event = event.get(msg['event'])
        if execute_event:
            execute_event()
            self.send_msg(
                origin="lixeira",destination="server",event="update", 
                data={'filled_percentage': self.filled_percentage(), "is_locked": self.is_locked })

    def fill(self, value: int):
        if self.isLocked:
            return
        elif value <= self.capacity - self.filled:
            self.filled += value
            if self.filled == self.capacity:
                self.lock()
        else:
            self.lock()
        self.send_msg(
            origin="lixeira",destination="server",event="update", 
            data={'filled_percentage': self.filled_percentage(), "is_locked": self.is_locked })
        
    def empty(self):
        self.filled = 0
        
    def lock(self):
        self.isLocked = True
        
    def unlock(self):
        self.isLocked = False

    def filled_percentage(self) -> float:
        return (self.filled * 100)/self.capacity

if __name__ == "__main__":
    from random import randint
    import time
    lixeira = Lixeira(500)
    with lixeira:
        while True:
            lixeira.await_for_msg()
            time.sleep(1)
            if not lixeira.isLocked:
                lixeira.fill(randint(30,70))