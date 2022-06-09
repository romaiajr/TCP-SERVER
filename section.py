import uuid
from mqtt_client import MQTTClient
import requests
import json
from random import randint

BASE_URL = "http://127.0.0.1:5000"
#Classe responsável por implementar o setor
class Section:

    def __init__(self, long, lat) -> None:
        self.id = str(uuid.uuid4())
        self.long = long
        self.lat = lat
        self.transhipment = None
        self.register()

    #Método responsável por registrar o setor no servidor
    def register(self):
        payload = {"id": str(self.id), "long": self.long, "lat": self.lat}
        response = requests.post(f'{BASE_URL}/register-section', json=payload)
        if response.status_code == 200:
            self.transhipment = Transhipment(self.id)
        else:
            print("Ocorreu um erro ao tentar registrar o setor")

#Classe responsável por implementar o transbordo
class Transhipment(MQTTClient):

    def __init__(self, id) -> None:
        MQTTClient.__init__(self, id)
        self.dumpsters = {}
        self.critical_dumpsters = {}
    
    #Método para lidar com mensagens mqtt
    def on_message(self,client, userdata, msg):
        event_dict = {'register': self.register_dumpster, 'update': self.update_dumpster}
        print(msg.payload)
        payload = json.loads(str(msg.payload.decode('utf-8')).replace("'",'"'))
        print(payload)
        execute = event_dict.get(payload['event'])
        if execute:
            execute(payload)

    #Método para registrar uma nova lixeira
    def register_dumpster(self, payload):
        self.dumpsters[payload['id']] = {"filled_percentage": 0, "isLocked": False, "id":payload['id']}
        print(self.dumpsters)

    #Método para atualizar uma lixeira
    def update_dumpster(self, payload):
        self.dumpsters[payload['id']] = payload['data']
        print(self.dumpsters)
        requests.post(f'{BASE_URL}/update-dumpster', json=self.dumpsters[payload['id']])

if __name__ == "__main__":
    section = Section(randint(0,50),randint(0,50))
    section.transhipment.subscribe()