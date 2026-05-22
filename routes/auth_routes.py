from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from Models.usuarios import Usuarios


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# REGISTER - cadastrar usuário
@auth_bp.route("/register", methods=["POST"])

def register():
    data = request.get_json()
    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")
    
    if not nome or not email or not senha:
        return jsonify({"message": "Nome, email e senha são obrigatórios."}), 400

    if len(senha) < 6: 
        return jsonify({"message": "A senha deve ter no mínimo 6 caracteres."}), 400

    usuario_existente = Usuarios.query.filter_by(email=email).first() # Verificar se já existe um usuário com o mesmo email

    if usuario_existente:
        return jsonify({"message": "Este email já está cadastrado."}), 400 

    senha_hash = generate_password_hash(senha) # Gerar hash da senha para segurança

    novo_usuario = Usuarios( # Criar novo usuário
        nome=nome,
        email=email,
        senha=senha_hash
    )

    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({
        "message": "Usuário cadastrado com sucesso!",
        "usuario": novo_usuario.as_dict()
    }), 201


# LOGIN - autenticar usuário
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"message": "Email e senha são obrigatórios."}), 400

    usuario = Usuarios.query.filter_by(email=email).first() # Buscar usuário pelo email para autenticação

    if not usuario:
        return jsonify({"message": "Email ou senha inválidos."}), 401 

# Verificar se a senha fornecida corresponde ao hash armazenado no banco de dados
    if not check_password_hash(usuario.senha, senha):
        return jsonify({"message": "Email ou senha inválidos."}), 401

    access_token = create_access_token(identity=str(usuario.id)) # Gerar token de acesso JWT usando o ID do usuário como identidade

    return jsonify({
        "message": "Login realizado com sucesso!",
        "access_token": access_token,
        "usuario": usuario.as_dict()
    }), 200


# ME - dados do usuário logado
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    usuario_id = get_jwt_identity()

    usuario = Usuarios.query.get(usuario_id)

    if not usuario:
        return jsonify({"message": "Usuário não encontrado."}), 404

    return jsonify({
        "usuario": usuario.as_dict()
    }), 200