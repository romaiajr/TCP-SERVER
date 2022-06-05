from mqtt_client import MQTTClient

class Truck(MQTTClient):

    def __init__(self):
        self.map = []

    def update_map(self, map):
        pass

    def collect_trash(self, topic):
        #Rodar intervalos de tempo x variados para coletar
        #self.publish_msg(dumbster, msg={"event": 'collect'})
        pass