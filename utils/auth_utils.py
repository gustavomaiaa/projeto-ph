from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from models.user import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()  # Verifica token válido e presente
            current_user_identity = get_jwt_identity()  # Pega identity do token
            claims = get_jwt()  # Pega claims do token, ex: role
            
            current_user = User.query.filter_by(username=current_user_identity).first()
            if not current_user:
                return jsonify({'message': 'Usuário não encontrado'}), 404
            
            current_role = claims.get('role', 'user')
        
        except Exception as e:
            return jsonify({'message': f'Erro na validação do token: {str(e)}'}), 403
        
        return f(current_user, current_role, *args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def wrapper(current_user, *args, **kwargs):
        if current_user.role != 'admin':
            return jsonify({'message': 'Acesso negado, administrador apenas'}), 403
        return f(current_user, *args, **kwargs)
    return wrapper
