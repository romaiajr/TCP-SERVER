from flask import Flask
app = Flask(__name__)

@app.route("/", methods=['GET'])
def health_check():
	return 'Caminhão Funcionando'

@app.route("/atualizar-mapa",  methods=['POST'])
def update_map():
	return 'Atualizar mapa de coleta'

if __name__ == "__main__":
	app.run()