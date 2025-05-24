from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/analise-falha', methods=['POST'])
def analisar_falha():
    data = request.get_json()
    nao_conformidade = data.get('nao_conformidade', '').lower()

    # Simulação da lógica de análise
    if any(palavra in nao_conformidade for palavra in ['freio', 'direção', 'airbag', 'falha estrutural']):
        resultado = {
            'classificacao': 'Crítica',
            'acao_recomendada': 'Recall',
            'descricao': 'Falha de segurança grave. Recall obrigatório.'
        }
    elif any(palavra in nao_conformidade for palavra in ['solda', 'pintura', 'acabamento', 'vedação']):
        resultado = {
            'classificacao': 'Média',
            'acao_recomendada': 'Notificação Oficial',
            'descricao': 'Problema relevante, notificar aos órgãos competentes.'
        }
    else:
        resultado = {
            'classificacao': 'Leve',
            'acao_recomendada': 'Nenhuma',
            'descricao': 'Falha menor, sem exigência de notificação.'
        }

    return jsonify(resultado), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
