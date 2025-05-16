from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from utils.auth_utils import token_required
from extensions import db  # ✅ CORRETO
from models.user import User
import jwt
import datetime
import uuid

SECRET_KEY = 'phobjectiveactive'  # depois mova isso para um arquivo config seguro


from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    senha = data.get('senha')

    if not username or not email or not senha:
        return jsonify({'message': 'Preencha todos os campos'}), 400

    # Verifica se o usuário já existe
    usuario_existente = User.query.filter_by(username=username).first()
    if usuario_existente:
        return jsonify({'message': 'Usuário já existe'}), 400

    # Cria o novo usuário com a senha hash
    senha_hash = generate_password_hash(senha)
    novo_usuario = User(username=username, email=email, senha_hash=senha_hash)

    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({'message': 'Usuário criado com sucesso'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    senha = data.get('senha')

    if not username or not senha:
        return jsonify({'message': 'Preencha todos os campos'}), 400

    usuario = User.query.filter_by(username=username).first()

    # CORRIGIDO AQUI: usar senha_hash
    if not usuario or not check_password_hash(usuario.senha_hash, senha):
        return jsonify({'message': 'Credenciais inválidas'}), 401

    token = jwt.encode({
        'public_id': usuario.public_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, SECRET_KEY, algorithm='HS256')

    return jsonify({'token': token}), 200
