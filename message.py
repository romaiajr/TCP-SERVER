import json

valid_entities = {"trash","server","adm","truck"}
#Classe com estrutura padrão para mensagens do protocolo desenvolvido
class Message():

    def __init__ (self, origin: str, destination: str, mac:str, event: str, data=None):
        self.origin = origin
        self.destination = destination
        self.mac = mac
        self.event = event
        self.data = data
    
    def get_msg(self):
        if self.validate_msg():
            return {"origin": self.origin, "destination": self.destination, "mac": self.mac, "event": self.event, "data": self.data}
        else:
            print("Wrong data supplied to Message")
    
    def validate_msg(self):
        return self.origin in valid_entities and self.destination in valid_entities 
