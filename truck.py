from flask import  jsonify
from mqtt_client import MQTTClient
import time
import random
import requests
from decouple import config as env

SERVER_URL = env('SERVER_URL')
#Classe que implementar o caminhão
class Truck(MQTTClient):

    def __init__(self):
        MQTTClient.__init__(self)
        self.map = []

    #Método para atualizar o mapa de coleta
    def update_map(self):
        try:
            response = requests.get(f'{SERVER_URL}/get-roadmap')
            if response:
                self.map = response.json()
                print(self.map)
            else:
                time.sleep(random.randint(3))
        except Exception as e:
            return jsonify({"msg": e})

    #Método coletar as lixeiras em n intervalos de tempo variados #TODO resolver problema de coleta entre tópicos
    def collect_trash(self):
        if len(self.map) >= 1:
            time.sleep(random.randint(3,8))
            dumpster = self.map.pop(0)     
            self.publish_msg(topic=dumpster["id"], msg={"event": 'collect'}, host=dumpster["host"], port=dumpster['port'])
        else:
            self.update_map()
            
if __name__ == "__main__":
    truck = Truck()
    while True:
        truck.collect_trash()
