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
        msg = self.recv_msg()
        if msg:
            msg_decoded = self.decode_msg(msg)
            print("Mensagem recebida: {}".format(msg_decoded))
            self.handle_msg(msg_decoded)
    
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
        
    def lock(self):
        self.is_locked = True
        
    def unlock(self):
        self.is_locked = False

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
            if not lixeira.is_locked:
                lixeira.fill(randint(30,70))