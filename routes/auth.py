from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from utils.auth_utils import token_required
from extensions import db  # ✅ CORRETO
from models.user import User
from datetime import datetime
import uuid
from utils.validacoes import validar_email


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
    nome = data.get('nome')
    data_nascimento_str = data.get('data_nascimento')
    role =data.get('role', 'user')

    # ✅ Verifica campos obrigatórios
    if not username or not email or not senha:
        return jsonify({'message': 'Preencha todos os campos obrigatórios'}), 400
    
    if not validar_email(email):
        return jsonify({'message': 'Preencha todos os campos obrigatórios'}), 400

    # ✅ Verifica se usuário já existe
    usuario_existente = User.query.filter_by(username=username).first()
    if usuario_existente:
        return jsonify({'message': 'Usuário já existe'}), 400

    # ✅ Gera hash da senha
    senha_hash = generate_password_hash(senha)

    print("Senha hash (len={}): {}".format(len(senha_hash), senha_hash))  

    # ✅ Converte data de nascimento
    data_nascimento = None
    if data_nascimento_str:
        try:
            data_nascimento = datetime.strptime(data_nascimento_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({'message': 'Formato de data inválido. Use YYYY-MM-DD'}), 400

    # ✅ Cria novo usuário
    novo_usuario = User(
        username=username,
        email=email,
        senha_hash=senha_hash,
        nome=nome,
        data_nascimento=data_nascimento,
        role=role
    )

    # ✅ Salva no banco de dados
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
    
    # Criando token com identidade e role no 'additional_claims'
    additional_claims = {"role": usuario.role}
    access_token = create_access_token(identity=usuario.username, additional_claims=additional_claims)

    acess_token = create_access_token(identity=usuario.username)

    return jsonify({'token': acess_token}), 200


@auth_bp.route('/usuarios', methods=['GET'])
@jwt_required()

def listar_usuarios():
    usuarios = User.query.all()
    return jsonify([
        {   
            "id":u.id,     
            "username": u.username,
            "nome": u.nome,
            "email": u.email,
            "data_nascimento": u.data_nascimento.isoformat() if u.data_nascimento else None
        } for u in usuarios
    ])