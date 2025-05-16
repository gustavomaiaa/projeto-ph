from functools import wraps
from flask import request, jsonify, current_app
from models.user import User
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token ausente'}), 403
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except Exception:
            return jsonify({'message': 'Token inválido'}), 403
        return f(current_user, *args, **kwargs)
    return decorated
