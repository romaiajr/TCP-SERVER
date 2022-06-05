import uuid
from mqtt_client import MQTTClient

class Section:

    def __init__(self, long, lat) -> None:
        self.id = uuid.uuid4()
        self.long = long
        self.lat = lat
        self.transhipment = None

    def self_register():
        #fazer post para API informando os dados do setor
        pass
    #quando der sucesso criar o transbordo

#Responsável pelo MQTT
class Transhipment(MQTTClient):

    def __init__(self, id) -> None:
        super.__init__(id)
        self.dumpsters = {}
        self.critical_dumpsters = []

    def on_message(self,client, userdata, msg):
        event_dict = {'register': self.register_dumpster, 'update': self.update_dumpster}
        payload = msg.payload
        execute = event_dict.get(payload['event'])
        execute(payload)

    def register_dumpster(self, payload):
        self.dumpsters[payload['id']] = {"filled_percentage": 0, "isLocked": False}

    def update_dumpster(self, payload):
        self.dumpsters[payload['id']] = payload['data']
        self.most_critical_dumpsters()

    def most_critical_dumpsters(self):
        aux = {}
        for dumpster in self.dumpsters:
            if dumpster["filled_percentage"] >= 80 or dumpster["is_locked"]:
                pass
        pass
        #sempre que algum lixo for atualizado, editar a lista de lixos e enviar para o servidor via POST