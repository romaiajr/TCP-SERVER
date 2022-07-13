import threading
from mqtt_client import MQTTClient
import requests
import time
import json
from random import randint
from decouple import config as env

SERVER_URL = env('SERVER_URL')
HOST = env('HOST')
PORT = int(env('PORT'))

# Classe responsável por implementar a lixeira
class Dumpster(MQTTClient):

    def __init__(self, lat, long, capacity) -> None:
        super().__init__()
        self.lat = lat
        self.long = long
        self.capacity = capacity
        self.filled = 0
        self.is_locked = False
        self.section = None
    
    #Método responsável por registrar a lixeira no setor
    def register(self):
        payload = {"long": self.long, "lat": self.lat}
        response = requests.post(f'{SERVER_URL}/register-dumpster', json=payload) #Rota para requisitar qual o setor mais próximo para conexão
        if response.status_code == 200:
            self.section = response.json()['id']
            self.publish(event='register')
            t1 = threading.Thread(target=self.subscribe)
            t2 = threading.Thread(target=self.fill)
            t1.start()
            t2.start()
        else:
            print("Ocorreu um erro ao tentar registrar a lixeira")
        
    #Método de encher a lixeira aleatóriamente em intervalos x de tempo
    def fill(self):
        while True:
            time.sleep(randint(2,6))
            value = randint(30, 100)
            if self.is_locked:
                return
            elif value <= self.capacity - self.filled:
                self.filled += value
                if self.filled == self.capacity:
                    self.lock()
            else:
                self.lock()
            self.publish(event='update', data={'filled_percentage': self.filled_percentage(), "is_locked": self.is_locked, "id": self.id, "host": HOST, "port": PORT}) 

    #Método para coleta da lixeira   
    def empty(self):
        self.filled = 0
        self.unlock()
        self.publish(event='update', data={'filled_percentage': self.filled_percentage(), "is_locked": self.is_locked, "id": self.id, "host": HOST, "port": PORT})

    #Método para travar a lixeira    
    def lock(self):
        self.is_locked = True

    #Método para destravar a lixeira    
    def unlock(self):
        self.is_locked = False

    #Método para calcular a % preenchida da lixeira
    def filled_percentage(self) -> float:
        return (self.filled * 100)/self.capacity
    
    #Método responsável por lidar com mensagens mqtt
    def on_message(self,client, userdata, msg):
        payload = json.loads(str(msg.payload.decode('utf-8')).replace("'",'"'))
        if payload['event'] == 'collect':
            self.empty()

    #Método responsável por publicar mensagens mqtt
    def publish(self, event, data={"host":HOST, "port":PORT}):
        print(self.section)
        if self.section:
            self.publish_msg(topic = self.section, msg={"id": self.id, "event": event, "data": data}, host=HOST, port=PORT)

#TODO rodar o on_message na thread
if __name__ == "__main__":
    dumpster = Dumpster(randint(0,50),randint(0,50),randint(200,500))
    dumpster.register()
  