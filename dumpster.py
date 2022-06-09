from mqtt_client import MQTTClient
import requests
BASE_URL = "http://127.0.0.1:5000"

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
        payload = {"long": self.long, "lat": self.lat}
        response = requests.post(f'{BASE_URL}/register-dumpster', json=payload)
        if response.status_code == 200:
            self.section = response.json()['id']
            self.publish(event='register')
        else:
            print("Ocorreu um erro ao tentar registrar a lixeira")
        
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
        print(msg)
        if msg.payload['event'] == 'collect':
            self.empty()
    
    def publish(self, event, data=None):
        if self.section:
            print(self.section)
            self.publish_msg(topic = self.section, msg={"id": self.id, "event": event, "data": data})

if __name__ == "__main__":
    dumpster = Dumpster(20,15,500)
    dumpster.register()
    dumpster.execute()