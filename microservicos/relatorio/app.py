from flask import Flask, jsonify
import requests

app = Flask(__name__)

# URLs dos microserviços
PRODUCAO_URL = "http://localhost:5001/ordem"
QUALIDADE_URL = "http://localhost:5002/inspecao"
PECAS_URL = "http://localhost:5003/componente"

@app.route('/relatorio/completo/<int:ordem_id>', methods=['GET'])
def relatorio_completo(ordem_id):
    relatorio = {}

    # 🔹 Consulta Produção
    prod_resp = requests.get(f"{PRODUCAO_URL}/{ordem_id}")
    if prod_resp.status_code != 200:
        return jsonify({'message': 'Ordem de produção não encontrada'}), 404
    ordem = prod_resp.json()
    relatorio['ordem_producao'] = ordem

    # 🔹 Consulta Inspeções relacionadas (buscando todas e filtrando localmente)
    insp_resp = requests.get(f"{QUALIDADE_URL}/todas")
    if insp_resp.status_code == 200:
        inspecoes = [i for i in insp_resp.json() if i['ordem_id'] == ordem_id]
    else:
        inspecoes = []
    relatorio['inspecoes'] = inspecoes

    return jsonify(relatorio)

@app.route('/relatorio/pecas/<int:id>', methods=['GET'])
def relatorio_pecas(id):
    # Passando o 'id' corretamente na URL
    response = requests.get(f"{PECAS_URL}/{id}")
    
    # Verificando se a resposta é válida e em formato JSON
    try:
        componentes = response.json()
        return jsonify(componentes)
    except ValueError:
        return jsonify({"message": "Resposta não é um JSON válido"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)
