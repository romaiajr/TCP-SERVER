from client import Client

class Lixeira(Client):

    def __init__(self, capacity: int) -> None:
        super().__init__()
        self.capacity = capacity
        self.filled = 0
        self.isLocked = False

    def create_msg(self):
        return {"client": "lixeira", "mac": self.mac, "filled_percentage": self.filled_percentage(), "isLocked": self.isLocked}

    def fill(self, value: int):
        if self.isLocked:
            return
        elif value <= self.capacity - self.filled:
            self.filled += value
            if self.filled == self.capacity:
                self.lock()
        else:
            self.lock()
        self.send_msg()
        
    def empty(self):
        self.filled = 0
        self.send_msg()
    
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
            if lixeira.isLocked:
                pass
            time.sleep(1)
            lixeira.fill(randint(30,50))
            print(lixeira.recv_msg())