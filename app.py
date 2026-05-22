import pymysql
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from db import db
from dotenv import load_dotenv
import os

load_dotenv()
#-------------------------------------------------------
# Imports dos models de cada tabela 
from Models.usuarios import Usuarios
from Models.categorias import Categorias
from Models.habitos import Habitos
from Models.metas import Metas
from Models.registros import Registros_habitos
#------------------------------------------------------

from flask_jwt_extended import JWTManager # Importa JWTManager para autenticação
#----------------------------------------------------------------

#importando os blueprints de cada rota 
from routes.usuarios import usuario_bp # Importa o Blueprint de usuários
from routes.categorias import categorias_bp # Importa o Blueprint de categorias
from routes.habitos import habitos_bp # Importa o Blueprint de hábitos
from routes.metas import metas_bp # Importa o Blueprint de metas
from routes.registros import registros_bp # Importa o Blueprint de registros
from routes.auth_routes import auth_bp # Importa o Blueprint de autenticação


#-------------------------------------------------------
# Cria a aplicação Flask
app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:Root#12345@localhost/ApiHabitos'

# inicializa o banco de dados e as migrações
db.init_app(app)
migrate = Migrate(app,db) 
#----------------------------------------
# registro de todos os blueprints 

app.register_blueprint(usuario_bp) 
app.register_blueprint(categorias_bp)
app.register_blueprint(habitos_bp)
app.register_blueprint(metas_bp)    
app.register_blueprint(registros_bp)
app.register_blueprint(auth_bp)
#-----------------------------------------

#Configura a chave secreta para JWT
jwt = JWTManager(app) # inicia JWTManager para autenticação

#-------------------------------------------------------

#rota principal
@app.route('/')
def BemVindo():
    return "Bem Vindo Usuario" # retorna mensagem

