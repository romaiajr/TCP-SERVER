from flask import Flask
from flask import request, jsonify
from math import dist
app = Flask(__name__)

class Server:
    def __init__(self):
        self.most_critical_dumpsters = {}
        self.sections = {}
        self.collect_map = {}
    
    def register_section(self,section):
        try:
            self.sections[section['id']] = section
            return jsonify({"msg": "Registered"}),200
        except Exception as e:
            return jsonify({"msg": e})

    def register_dumpster(self, coordinate):
        try:
            if self.sections:
                best_section = None
                lower_dist = 50000
                for section in self.sections.values():
                    current_dist = dist([section['lat'], section['long']], [coordinate['lat'], coordinate['long']])
                    if current_dist < lower_dist:
                        best_section = section['id']
                        lower_dist = current_dist
                return jsonify({"id": best_section}), 200
            else:
                return jsonify({"msg": "Nenhum setor cadastrado"}), 400
        except Exception as e:
            print(e)
            return jsonify({"msg": e})

    def get_dumpster(self, id):
        try:
            dumpster = self.most_critical_dumpsters.get(id)
            if dumpster:
                return jsonify({"lixeira": dumpster})
            else:
                return jsonify({"msg": "Lixeira não encontrada"}),404
        except Exception as e:
            return jsonify({"msg": e})

    def get_dumpsters(self):
        return self.most_critical_dumpsters

    #TODO
    def update_dumpsters():
        pass

    #TODO
    def build_collect_map():
        pass

server = Server()

@app.route("/", methods=['GET'])
def health_check():
	return 'Servidor Funcionando'

@app.route("/dumpster/<id>",  methods=['GET'])
def get_dumpster(id):
    print(id)
    return server.get_dumpster(id)

@app.route("/dumpsters/<qtd>",  methods=['GET'])
def get_most_critical_dumpsters(qtd):
    print(qtd)
    return server.get_dumpsters()

#TODO
@app.route("/update-dumpsters",  methods=['POST'])
def update_dumpsters():
    print(request['data'])
    return server.update_dumpsters()

@app.route("/register-dumpster",  methods=['POST'])
def register_dumpster():
    return server.register_dumpster(request.json)

@app.route("/register-section",  methods=['POST'])
def register_section():
    return server.register_section(request.json)

if __name__ == "__main__":
    app.run()