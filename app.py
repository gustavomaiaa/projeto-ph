from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from extensions import db
import os
from dotenv import load_dotenv

load_dotenv()


# Criação da aplicação
app = Flask(__name__)
CORS(app)

# Configurações diretamente no código
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if not app.config['JWT_SECRET_KEY'] or not app.config['SQLALCHEMY_DATABASE_URI']:
    raise RuntimeError("Variáveis de ambiente não carregadas corretamente.")

# Inicialização das extensões
db.init_app(app)
jwt = JWTManager(app)

# Importação e registro de blueprints
from routes.medicoes import medicoes_bp
from routes.auth import auth_bp

# Adiciona prefixo para evitar conflitos e facilitar testes
app.register_blueprint(medicoes_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')

# Rota básica para teste
@app.route('/')
def index():
    return "Sistema de pH ativo! Seja bem-vindo(a)!"

# Inicialização do servidor
if __name__ == '__main__':
    app.run(debug=True)
