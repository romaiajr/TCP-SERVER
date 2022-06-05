from flask import Flask
app = Flask(__name__)


class Server:
    def __init__(self):
        self.most_critical_dumpsters = []
        self.sections = []
        self.collect_map = []
    
    def register_section(section):
        pass

    def registrer_dumpster(coordinate):
        #olhar qual a melhor sessão para o dumpster
        pass

    def get_dumpster(id):
        pass

    def get_dumpsters():
        pass

    def update_dumpsters():
        pass

@app.route("/", methods=['GET'])
def health_check():
	return 'API Funcionando'

@app.route("/dumpster/<id>",  methods=['GET'])
def get_dumpster(id):
	return id

@app.route("/dumpsters/<qtd>",  methods=['GET'])
def get_most_critical_dumpsters(qtd):
	return "get_most_critical_dumpsters"

@app.route("/update-most-critical-dumpsters",  methods=['POST'])
def update_most_critical_dumpsters():
	return "atualizar lixeiras críticas"

@app.route("/register-dumpster/<coordinate>",  methods=['GET'])
def register_dumpster(coordinate):
	return coordinate

@app.route("/register-section",  methods=['POST'])
def register_section():
	return "registrar setor"

if __name__ == "__main__":
	app.run()