import uuid
import paho.mqtt.client as mqtt
import threading


#Classe responsável por implementar o MQTT
class MQTTClient:

    def __init__(self,id = None) -> None:
        self.id = id if id else str(uuid.uuid4()) # Identificador único para todo cliente mqtt, representando seu tópico
        self.client = mqtt.Client()
        print(self.id)
        
    def on_connect(self,client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe(str(self.id))
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_message(self, client, userdata, msg):
        mensagem = str(msg.payload.decode("utf-8"))
        print(mensagem)
        
    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("localhost", 1883, 60)
        self.client.loop_forever()

    def publish_msg(self, topic, msg):
        print(topic, msg)
        self.client.publish(topic, str(msg))
        self.client.loop_start()

if __name__ == "__main__":
    mqtt = MQTTClient()
    mqtt.connect()