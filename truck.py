from flask import Flask
from flask import request,jsonify
from mqtt_client import MQTTClient
import time
import random

app = Flask(__name__)

#Classe que implementar o caminhão
class Truck(MQTTClient):

    def __init__(self):
        MQTTClient.__init__(self)
        self.map = []

    #Método para atualizar o mapa de coleta
    def update_map(self, map):
        try:
            self.map = map
            print(self.map)
            return jsonify({"msg": "Mapa de coleta atualizado"}),200
        except Exception as e:
            return jsonify({"msg": e})

    #Método coletar as lixeiras em n intervalos de tempo variados
    #TODO rodar em paralelo à API num while true
    def collect_trash(self, topic):
        if self.collect_trash:
            time.sleep(random.randint(3,8))
            dumpster = self.map.pop(0)     
            self.publish_msg(dumpster, msg={"event": 'collect'})

truck = Truck()

@app.route("/", methods=['GET'])
def health_check():
	return 'Caminhão Funcionando'

@app.route("/update-map",  methods=['POST'])
def update_map():
    print(request.json)
    return truck.update_map(request.json)

if __name__ == "__main__":
	app.run(port=5050)