from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Armazenamento em memória
componentes = []

@app.route('/componente', methods=['POST'])
def registrar_componente():
    data = request.get_json()
    novo_componente = {
        'id': len(componentes) + 1,
        'nome': data['nome'],
        'veiculo_id': data['veiculo_id'],
        'quantidade': data['quantidade']
    }
    componentes.append(novo_componente)
    return jsonify({'message': 'Componente registrado com sucesso'}), 201

@app.route('/componente/<int:id>', methods=['GET'])
def obter_componente(id):
    componente = next((c for c in componentes if c['id'] == id), None)
    if componente is None:
        return jsonify({'message': 'Componente não encontrado'}), 404
    return jsonify(componente)

@app.route('/componente/veiculo/<int:veiculo_id>', methods=['GET'])
def obter_componentes_por_veiculo(veiculo_id):
    comps = [c for c in componentes if c['veiculo_id'] == veiculo_id]
    return jsonify(comps)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
