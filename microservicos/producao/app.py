from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Armazenamento em memória
ordens_producao = []

@app.route('/ordem', methods=['POST'])
def criar_ordem():
    data = request.get_json()
    nova_ordem = {
        'id': len(ordens_producao) + 1,
        'status': data['status'],
        'etapa': data['etapa'],
        'descricao': data['descricao'], 
    }
    ordens_producao.append(nova_ordem)
    return jsonify({'message': 'Ordem de produção criada com sucesso'}), 201


@app.route('/ordem/<int:id>', methods=['GET'])
def obter_ordem(id):
    ordem = next((o for o in ordens_producao if o['id'] == id), None)
    if ordem is None:
        return jsonify({'message': 'Ordem não encontrada'}), 404
    return jsonify(ordem)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
