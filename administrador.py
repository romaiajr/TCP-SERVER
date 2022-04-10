from client import Client

class Administrador(Client):

    def __init__(self) -> None:
        super().__init__()
        self.lixeiras = {}
        self.to_collect = []
    
    def await_for_msg(self) -> None:
        self.send_msg(type="connect")
        while True:
            try:
                msg = self.recv_msg()
                if msg:
                    print(msg)
                    self.handle_msg(msg)
            except Exception as e:
                print(e)
    
    def create_msg(self, **kwargs):
        msg = {"client": "adm", "mac": self.mac, "type": kwargs.get('type')}
        if kwargs.get("type") == 'send_to_collect':
            msg['to_collect'] = self.to_collect
        return msg

    def handle_msg(self, msg):
        self.lixeiras = self.decode_msg(msg)
        for key in self.lixeiras:
            lixeira = self.lixeiras[key]
            if (lixeira['isLocked'] or int(lixeira['filled_percentage']) >= 80) and key not in self.to_collect:
                self.to_collect.append(key)
                self.send_msg(type="send_to_collect")

if __name__ == "__main__":
    adm = Administrador()
    with adm:
        adm.await_for_msg()
        
        
        