from flask import Flask
from flask import request, jsonify
from math import dist
BASE_URL_TRUCK = "http://127.0.0.1:5050"
import requests
app = Flask(__name__)

class Server:
    def __init__(self):
        self.most_critical_dumpsters = {}
        self.sections = {}
        self.collect_map = []
    
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
    def update_dumpsters(self, payload):
        self.most_critical_dumpsters[payload['id']] = payload['data']
        self.sort_critial_dumpsters()
        self.collect_map()

    def sort_critial_dumpsters(self):
        collect_map = []
        dumpstersList = [] 
        critical_dumpsters = {}
        for dumpster in self.most_critical_dumpsters.keys():
            insert = self.most_critical_dumpsters[dumpster]
            insert['id'] = dumpster
            dumpstersList.append(insert)
        dumpstersList = sorted(dumpstersList,reverse=True, key=lambda k : k['filled_percentage'])
        for dumpster in dumpstersList:
            collect_map.append(dumpster["id"])
            critical_dumpsters[dumpster["id"]] = dumpster
        self.most_critical_dumpsters = critical_dumpsters
        self.collect_map = collect_map

    #TODO
    def build_collect_map(self):
        response = requests.post(f'{BASE_URL_TRUCK}/update-dumpster', json=self.collect_map)

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
    return server.update_dumpsters(request.json)

@app.route("/register-dumpster",  methods=['POST'])
def register_dumpster():
    return server.register_dumpster(request.json)

@app.route("/register-section",  methods=['POST'])
def register_section():
    return server.register_section(request.json)

if __name__ == "__main__":
    app.run()