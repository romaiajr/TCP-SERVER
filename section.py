import uuid
from mqtt_client import MQTTClient
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

class Section:

    def __init__(self, long, lat) -> None:
        self.id = str(uuid.uuid4())
        self.long = long
        self.lat = lat
        self.transhipment = None
        self.register()

    def register(self):
        payload = {"id": str(self.id), "long": self.long, "lat": self.lat}
        response = requests.post(f'{BASE_URL}/register-section', json=payload)
        if response.status_code == 200:
            self.transhipment = Transhipment(self.id)
        else:
            print("Ocorreu um erro ao tentar registrar o setor")

#Responsável pelo MQTT
class Transhipment(MQTTClient):

    def __init__(self, id) -> None:
        MQTTClient.__init__(self, id)
        self.dumpsters = {}
        self.critical_dumpsters = {}
    
    def on_message(self,client, userdata, msg):
        event_dict = {'register': self.register_dumpster, 'update': self.update_dumpster}
        payload = json.loads(msg.payload.decode())
        execute = event_dict.get(payload['event'])
        if execute:
            execute(payload)

    def register_dumpster(self, payload):
        self.dumpsters[payload['id']] = {"filled_percentage": 0, "isLocked": False, "id":payload['id']}
        print(self.dumpsters)

    def update_dumpster(self, payload):
        self.dumpsters[payload['id']] = payload['data']
        print(self.dumpsters)
        requests.post(f'{BASE_URL}/update-dumpster', json=self.dumpsters[payload['id']])

if __name__ == "__main__":
    section = Section(20,30)
    section.transhipment.connect()