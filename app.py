from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from extensions import db

# Criação da aplicação
app = Flask(__name__)
CORS(app)

# Configurações diretamente no código
app.config['SECRET_KEY'] = 'phobjectiveactive'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:16112004@localhost/ph_agua'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização das extensões
db.init_app(app)
jwt = JWTManager(app)

# Importação e registro de blueprints
from routes.medicoes import medicoes_bp
from routes.auth import auth_bp

# Adiciona prefixo para evitar conflitos e facilitar testes
app.register_blueprint(medicoes_bp, url_prefix='/medicoes')
app.register_blueprint(auth_bp, url_prefix='/auth')

# Rota básica para teste
@app.route('/')
def index():
    return "Sistema de pH ativo! Seja bem-vindo(a)!"

# Inicialização do servidor
if __name__ == '__main__':
    app.run(debug=True)
