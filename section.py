import uuid
from mqtt_client import MQTTClient
import requests
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
        print(msg)
        event_dict = {'register': self.register_dumpster, 'update': self.update_dumpster}
        payload = msg.payload
        execute = event_dict.get(payload['event'])
        if execute:
            execute(payload)

    def register_dumpster(self, payload):
        self.dumpsters[payload['id']] = {"filled_percentage": 0, "isLocked": False}

    def update_dumpster(self, payload):
        self.dumpsters[payload['id']] = payload['data']
        self.most_critical_dumpsters()

    #TODO
    def most_critical_dumpsters(self):
        dumpstersList = [] 
        critical_dumpsters = {}
        for dumpster in self.dumpsters.keys():
            insert = self.dumpsters[dumpster]
            insert['id'] = dumpster
            dumpstersList.append(insert)
        dumpstersList = sorted(dumpstersList,reverse=True, key=lambda k : k['filled_percentage'])
        for dumpster in dumpstersList:
            critical_dumpsters[dumpster["id"]] = dumpster
        self.critical_dumpsters = critical_dumpsters

if __name__ == "__main__":
    section = Section(20,30)