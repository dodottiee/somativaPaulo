from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Armazenamento em memória
inspecoes = []

# URL do serviço de Produção
PRODUCAO_URL = "http://localhost:5001/ordem"

@app.route('/inspecao', methods=['POST'])
def criar_inspecao():
    data = request.get_json()

    # Verifica se a ordem de produção existe
    ordem_id = data.get('ordem_id')
    if not ordem_id:
        return jsonify({'message': 'ordem_id é obrigatório'}), 400

    response = requests.get(f"{PRODUCAO_URL}/{ordem_id}")
    if response.status_code != 200:
        return jsonify({'message': 'Ordem de produção não encontrada'}), 404

    ordem = response.json()

    nova_inspecao = {
        'id': len(inspecoes) + 1,
        'ordem_id': ordem_id,
        'status': data['status'],
        'nao_conformidade': data.get('nao_conformidade'),
        'descricao_ordem': ordem['descricao']  # Exemplo de dado trazido da Produção
    }
    inspecoes.append(nova_inspecao)
    return jsonify({'message': 'Inspeção registrada com sucesso', 'inspecao': nova_inspecao}), 201

@app.route('/inspecao/<int:id>', methods=['GET'])
def obter_inspecao(id):
    inspecao = next((i for i in inspecoes if i['id'] == id), None)
    if inspecao is None:
        return jsonify({'message': 'Inspeção não encontrada'}), 404
    return jsonify(inspecao)

@app.route('/inspecao/todas', methods=['GET'])
def listar_inspecoes():
    return jsonify(inspecoes)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
