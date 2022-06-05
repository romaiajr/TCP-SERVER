import uuid
import paho.mqtt.client as mqtt

class MQTTClient:

    def __init__(self,id = None) -> None:
        self.id = id if id else uuid.uuid4()
        self.client = mqtt.Client()

    def on_connect(self,client, userdata, flags, rc):
        client.subscribe(str(self.id))

    #Sobrescrever de acordo com cada cliente
    def on_message(self,client, userdata, msg):
        pass

    def publish_msg(self, topic, msg):
        self.client.publish(topic, msg)

    def __enter__(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("localhost", 1883, 60)
        self.client.loop_forever()
    
    def __exit__(self):
        self.client._clean_session()