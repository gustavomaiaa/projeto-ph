from flask import Blueprint, request, jsonify
from db_config import conectar_ao_banco
from utils.logs import logger  # Importando o logger
from utils.validacoes import validar_ph  # Importando a função de validação
from datetime import datetime
import traceback
import pymysql
from utils.auth_utils import token_required



medicoes_bp = Blueprint('medicoes', __name__)

# POST /medicoes → adicionar nova medição
@medicoes_bp.route('/medicoes', methods=['POST'])
@token_required 
def adicionar_medicao():
    dados = request.get_json()
    ph = dados.get('ph')

    if ph is None:
        logger.error("Tentativa de adicionar medição sem valor de pH")
        return jsonify({'erro': 'Valor de pH não fornecido'}), 400

    # ✅ Validação do tipo e faixa do valor de pH
    valido, resultado = validar_ph(ph)
    if not valido:
        logger.error(f"Valor de pH inválido: {resultado}")
        return jsonify({'erro': resultado}), 400
    ph = resultado  # ph agora é float validado

    try:
        con = conectar_ao_banco()
        cursor = con.cursor()
        cursor.execute("INSERT INTO medicoes (ph) VALUES (%s)", (ph,))
        con.commit()
        con.close()
        logger.info(f"Medição adicionada com sucesso: pH = {ph}")
        return jsonify({'mensagem': 'Medição adicionada com sucesso'}), 201
    except Exception as e:
        logger.error(f"Erro ao adicionar medição: {str(e)}", exc_info=True)
        return jsonify({'erro': str(e)}), 500

# GET /medicoes
@medicoes_bp.route('/medicoes', methods=['GET'])
@token_required
def obter_ultima_medicao():
    try:
        con = conectar_ao_banco()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT ph, data_hora FROM medicoes ORDER BY id DESC LIMIT 1")
        resultado = cursor.fetchone()
        con.close()

        if resultado:
            ph = resultado['ph']
            data_hora = resultado['data_hora']
            return jsonify({'ph': ph, 'data_hora': str(data_hora)})
        else:
            return jsonify({'mensagem': 'Nenhuma medição encontrada'}), 404

    except Exception as e:
        import traceback
        return jsonify({'erro': traceback.format_exc()}), 500

        # GET /medicoes/todas
@medicoes_bp.route('/medicoes/todas', methods=['GET'])
@token_required
def listar_todas_medicoes():
    try:
        con = conectar_ao_banco()
        print("Conexão bem-sucedida com o banco de dados.")
        cursor = con.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, ph, data_hora FROM medicoes ORDER BY id DESC")
        resultados = cursor.fetchall()
        print(f"RESULTADOS: {resultados}")
        print(f"TIPO DO DADO DE DATA: {type(resultados[0]['data_hora'])}")

        print(f"RESULTADOS RECUPERADOS: {resultados}")  # Verificando os dados do banco de dados
        
        if resultados:
            medicoes = [
                {
                    'id': row['id'],
                    'ph': row['ph'],
                    'data_hora': row['data_hora'].strftime('%Y-%m-%d %H:%M:%S') if isinstance(row['data_hora'], datetime) else str(row['data_hora'])
                }
                for row in resultados
            ]
            print(f"Dados formatados para retorno: {medicoes}")
            return jsonify(medicoes)
        else:
            print("Nenhum resultado encontrado.")
            return jsonify({'erro': 'Nenhuma medição encontrada'}), 404
   
    except Exception as e:
       logger.error("Erro ao listar medições", exc_info=True)
       print(f"EXCEÇÃO: {e} - {type(e)}")
       print(traceback.format_exc())  # Mostra o erro detalhado no terminal
       return jsonify({'erro': traceback.format_exc()}), 500



    
    # DELETE /medicoes/<id>
@medicoes_bp.route('/medicoes/<int:id>', methods=['DELETE'])
@token_required
def deletar_medicao(id):
    try:
        con = conectar_ao_banco()
        cursor = con.cursor()
        cursor.execute("DELETE FROM medicoes WHERE id = %s", (id,))
        con.commit()
        con.close()

        if cursor.rowcount == 0:
            return jsonify({'mensagem': 'Medição não encontrada'}), 404

        return jsonify({'mensagem': 'Medição excluída com sucesso'}), 200
    except Exception as e:
        logger.error(f"Erro ao deletar medição com ID {id}", exc_info=True)
        return jsonify({'erro': str(e)}), 500


