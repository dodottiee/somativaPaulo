from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Armazenamento em memória
inspecoes = []

# URL do serviço externo Certificadora Nacional de Qualidade (CNQ)
PRODUCAO_URL = "http://producao:5000/ordem"
CERTIFICADORA_URL = "http://certificadora:5000/analise-falha"

def consultar_certificadora(nao_conformidade):
    """Faz a consulta à Certificadora Nacional de Qualidade"""
    try:
        response = requests.post(
            CERTIFICADORA_URL,
            json={'nao_conformidade': nao_conformidade},
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {
                'classificacao': 'Desconhecido',
                'acao_recomendada': 'Erro na certificadora',
                'descricao': 'Não foi possível obter análise'
            }
    except Exception as e:
        return {
            'classificacao': 'Desconhecido',
            'acao_recomendada': 'Falha na comunicação',
            'descricao': str(e)
        }

@app.route('/inspecao', methods=['POST'])
def criar_inspecao():
    data = request.get_json()

    # Obter a análise da certificadora, se houver não conformidade
    if 'nao_conformidade' in data and data['nao_conformidade']:
        analise_certificadora = consultar_certificadora(data['nao_conformidade'])
    else:
        analise_certificadora = None

    ordem_id = data.get('ordem_id')
    if not ordem_id:
        return jsonify({'message': 'ordem_id é obrigatório'}), 400

    response = requests.get(f"{PRODUCAO_URL}/{ordem_id}")
    if response.status_code != 200:
        return jsonify({'message': 'Ordem de produção não encontrada'}), 404

    nova_inspecao = {
        'id': len(inspecoes) + 1,
        'ordem_id': ordem_id,
        'status': data['status'],
        'nao_conformidade': data.get('nao_conformidade'),
        'analise_certificadora': analise_certificadora  # Adiciona a análise ao registro
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
    app.run(debug=True, host='0.0.0.0', port=5000)