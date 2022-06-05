from flask import Flask
from mqtt_client import MQTTClient

app = Flask(__name__)

class Truck(MQTTClient):

    def __init__(self):
        self.map = []

    def update_map(self, map):
        pass

    def collect_trash(self, topic):
        #Rodar intervalos de tempo x variados para coletar
        #self.publish_msg(dumbster, msg={"event": 'collect'})
        pass

@app.route("/", methods=['GET'])
def health_check():
	return 'Caminhão Funcionando'

@app.route("/atualizar-mapa",  methods=['POST'])
def update_map():
	return 'Atualizar mapa de coleta'



if __name__ == "__main__":
	app.run()