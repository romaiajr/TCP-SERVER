from flask import Flask
app = Flask(__name__)

@app.route("/", methods=['GET'])
def health_check():
	return 'API Funcionando'

@app.route("/dumpster/<id>",  methods=['GET'])
def get_dumpster(id):
	return id

@app.route("/dumpsters",  methods=['GET'])
def get_most_critical_dumpsters():
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