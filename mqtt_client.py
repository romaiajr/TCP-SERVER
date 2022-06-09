import uuid
import paho.mqtt.client as mqtt

class MQTTClient:

    def __init__(self,id = None) -> None:
        self.id = id if id else str(uuid.uuid4())
        self.client = mqtt.Client()

    def on_connect(self,client, userdata, flags, rc):
        client.subscribe(str(self.id))

    #Sobrescrever de acordo com cada cliente
    def on_message(self,client, userdata, msg):
        print(msg)

    def publish_msg(self, topic, msg):
        print(topic, msg)
        self.client.publish(topic, str(msg))

    def execute(self):
        print(self.id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("localhost", 1884, 60)
        self.client.loop_forever()

if __name__ == "__main__":
    mqtt = MQTTClient()
    mqtt.execute() 