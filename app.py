import pymysql
from flasgger import Swagger
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from db import db
from dotenv import load_dotenv
import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager

load_dotenv()

# -------------------------------------------------------
# Imports dos models de cada tabela
from Models.usuarios import Usuarios
from Models.categorias import Categorias
from Models.habitos import Habitos
from Models.metas import Metas
from Models.registros import Registros_habitos
# -------------------------------------------------------

# Importando os blueprints de cada rota
from routes.usuarios import usuario_bp
from routes.categorias import categorias_bp
from routes.habitos import habitos_bp
from routes.metas import metas_bp
from routes.registros import registros_bp
from routes.auth_routes import auth_bp


# -------------------------------------------------------
# Cria a aplicação Flask
app = Flask(__name__)

# Evita erro de redirect com barra final
app.url_map.strict_slashes = False

# Configura CORS
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Configurações do banco
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/ApiHabitos"

# Chave usada para gerar e validar tokens JWT
app.config["JWT_SECRET_KEY"] = "minha_chave_secreta_super_segura"


# -------------------------------------------------------
# Configuração do Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API de Hábitos",
        "description": "Documentação da API REST de Hábitos com Flask, JWT, paginação e CRUDs.",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": ["http"],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Digite: Bearer SEU_TOKEN_JWT"
        }
    }
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)


# -------------------------------------------------------
# Inicializa o banco de dados, migrações e JWT
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)


# -------------------------------------------------------
# Registro de todos os blueprints
app.register_blueprint(usuario_bp)
app.register_blueprint(categorias_bp)
app.register_blueprint(habitos_bp)
app.register_blueprint(metas_bp)
app.register_blueprint(registros_bp)
app.register_blueprint(auth_bp)


# -------------------------------------------------------
# Rota principal
@app.route("/")
def BemVindo():
    return "Bem Vindo Usuario"