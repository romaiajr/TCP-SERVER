from mqtt_client import MQTTClient

class Dumpster(MQTTClient):

    def __init__(self, lat, long, capacity) -> None:
        super().__init__()
        self.lat = lat
        self.long = long
        self.capacity = capacity
        self.filled = 0
        self.is_locked = False
        self.section = None
    
    def register(self):
        #fazer get para a API e ver qual a section
        self.publish(event='register')
        
    def fill(self, value: int):
        if self.is_locked:
            return
        elif value <= self.capacity - self.filled:
            self.filled += value
            if self.filled == self.capacity:
                self.lock()
        else:
            self.lock()
        self.publish(event='update', data={'filled_percentage': self.filled_percentage(), "is_locked": self.is_locked})
        
    def empty(self):
        self.filled = 0
        self.unlock()
        self.publish(event='update', data={'filled_percentage': self.filled_percentage(), "is_locked": self.is_locked})
        
    def lock(self):
        self.is_locked = True
        
    def unlock(self):
        self.is_locked = False

    def filled_percentage(self) -> float:
        return (self.filled * 100)/self.capacity
    
    def on_message(self,client, userdata, msg):
        if msg.payload['event'] == 'collect':
            self.empty()
    
    def publish(self, event, data=None):
        if self.section:
            self.publish_msg(self.section, msg={"id": self.id, "event": event, "data": data})

if __name__ == "__main__":
    import time
    dumpster = Dumpster(1,1,500)
    print(dumpster.id)
    with dumpster:
        while True:
            time.sleep(3)
            print("Okay")
            #Encher em intervalos x de tempo variados e com valores variados