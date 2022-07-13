from flask import Flask
from flask import request, jsonify
from math import dist
import requests
app = Flask(__name__)
BASE_URL_ROBERTO = "http://25.2.231.195:5000"
BASE_URL_DANIEL_LENOVO = "http://25.2.240.249:5000"
BASE_URL_DANIEL_ACER = "http://25.3.139.238:5000"

#Classe responsável por implementar o servidor
class Server:
    def __init__(self):
        self.most_critical_dumpsters = {}
        self.section = None
        self.collect_map = []
    
    #Método para registrar um novo setor
    def register_section(self,section):
        try:
            self.section = section['id']
            print(self.section)
            return jsonify({"msg": "Registered"}),200
        except Exception as e:
            return jsonify({"msg": e})

    #Método para retornar o melhor setor para uma lixeira de acordo com a distância euclidiana
    def register_dumpster(self, coordinate):
        try:
            return jsonify({"id": self.section}), 200
        except Exception as e:
            print(e)
            return jsonify({"msg": e})

    #Método para retornar uma lixeira x a partir do ID
    def get_dumpster(self, id):
        try:
            dumpster = self.most_critical_dumpsters.get(id)
            if dumpster:
                return jsonify({"lixeira": dumpster})
            else:
                return jsonify({"msg": "Lixeira não encontrada"}),404
        except Exception as e:
            return jsonify({"msg": e})

    #Método para retornar n lixeiras do array
    def get_dumpsters(self, n):
        if int(n) < len(self.most_critical_dumpsters):
            return self.most_critical_dumpsters[0:n]
        return self.most_critical_dumpsters

    #Método para atualizar as lixeiras do servidor
    def update_dumpsters(self, payload):
        try:
            self.most_critical_dumpsters[payload['id']] = payload
            self.sort_critical_dumpsters()
            return jsonify({"msg": "Lixeira atualizada com sucesso"}), 200
        except Exception as e:
            return jsonify({"msg": e})

    #Método para ordenar as lixeiras da mais crítica do setor
    def sort_critical_dumpsters(self):
        collect_map = []
        dumpstersList = [] 
        critical_dumpsters = {}
        for dumpster in self.most_critical_dumpsters.keys():
            insert = self.most_critical_dumpsters[dumpster]
            insert['id'] = dumpster
            dumpstersList.append(insert)
        dumpstersList = sorted(dumpstersList,reverse=True, key=lambda k : k['filled_percentage'])
        for dumpster in dumpstersList:
            collect_map.append(dumpster)
            critical_dumpsters[dumpster["id"]] = dumpster
        self.most_critical_dumpsters = critical_dumpsters
        self.collect_map = collect_map

    #montar a lista de lixeiras para coleta entre todos os setores
    #TODO
    def get_roadmap(self):
        setor2 = requests.get(f'{BASE_URL_DANIEL_ACER}/get-collect-map')
        setor3 = requests.get(f'{BASE_URL_DANIEL_LENOVO}/get-collect-map')
        all_sectors_map = self.collect_map + setor2.json() + setor3.json()
        # collect_map = self.sort_most_critical_dumpsters(all_sectors_map)
        return jsonify(all_sectors_map)

    def get_collect_map(self):
        return jsonify(self.collect_map)
    
    def sort_most_critical_dumpsters(self, list):
        #ordenar e pegar as 5 primeiras
        for dumpster in self.most_critical_dumpsters.keys():
            insert = self.most_critical_dumpsters[dumpster]
            insert['id'] = dumpster
            dumpstersList.append(insert)
        dumpstersList = sorted(dumpstersList,reverse=True, key=lambda k : k['filled_percentage'])
        for dumpster in dumpstersList:
            collect_map.append(dumpster)
            critical_dumpsters[dumpster["id"]] = dumpster

server = Server()

@app.route("/", methods=['GET'])
def health_check():
	return 'Servidor Funcionando'

@app.route("/dumpster/<id>",  methods=['GET'])
def get_dumpster(id):
    return server.get_dumpster(id)

@app.route("/dumpsters/<qtd>",  methods=['GET'])
def get_most_critical_dumpsters(qtd):
    return server.get_dumpsters(qtd)

@app.route("/update-dumpster",  methods=['POST'])
def update_dumpsters():
    print(request.json)
    return server.update_dumpsters(request.json)

@app.route("/register-dumpster",  methods=['POST'])
def register_dumpster():
    return server.register_dumpster(request.json)

@app.route("/register-section",  methods=['POST'])
def register_section():
    return server.register_section(request.json)

#TODO
@app.route("/get-roadmap",  methods=['GET'])
def get_roadmap():
    return server.get_roadmap()

@app.route("/get-collect-map",  methods=['GET'])
def get_collect_map():
    return server.get_collect_map()

if __name__ == "__main__":
    app.run(host="25.2.231.195", port=5000)