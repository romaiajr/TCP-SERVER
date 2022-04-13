import json

valid_origin = {"trash","server","adm","truck"}
valid_destination = {"trash","server","truck", "adm"}   
valid_events_for_trash = {"register","update"}
valid_events_for_adm = {"register","update_list_of_trash", "lock_trash", "unlock_trash"}
valid_events_for_truck = {"register", "collect_trash"}
valid_events_for_server = {"update_list_to_collect", "collect_trash"}

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
        if self.origin not in valid_origin or self.destination not in valid_destination: 
            return False
        validate_event = {
            "trash": self.event in valid_events_for_trash, 
            "truck": self.event in valid_events_for_truck, 
            "adm": self.event in valid_events_for_adm,
            "server": self.event in valid_events_for_server}
        result = validate_event.get(self.origin)
        return result
        
if __name__ == "__main__":
    msg = Message("truck","trash","18111240121212","collect_trash")
    print(msg.get_msg())
    msg = str.encode(json.dumps(msg.get_msg()))
    print(json.loads(msg.decode('utf-8')))
