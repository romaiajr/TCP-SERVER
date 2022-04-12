valid_origin = set("trash","server","adm","truck")
valid_destination = set("trash","server","truck")
valid_events_for_trash = set("register","update")
valid_events_for_adm = set("register","update_list_of_trash", "lock_trash", "unlock_trash")
valid_events_for_truck = set("register","update_list_to_collect", "collect_trash")

class Message():

    def __init__ (self, origin: str, destination: str, event: str, **data):
        self.origin = origin
        self.destination = destination
        self.event = event
        self.data = data
    
    def get_msg(self):
        if self.validate_msg():
            return {"origin": self.origin, "destination": self.destination, "event": self.event, "data": self.data}
        else:
            print("Wrong data supplied to Message")
    
    def validate_msg(self):
        if self.origin not in valid_origin or self.destination not in valid_destination: 
            return False
        validate_event = {
            "trash": self.event in valid_events_for_trash, 
            "truck": self.event in valid_events_for_truck, 
            "adm": self.event in valid_events_for_adm}
        return validate_event.get(self.destination)
        
if __name__ == "__main__":
    Message("truck","server","clear",mac=18111240121212)
