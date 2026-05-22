from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from db import db
from Models.usuarios import Usuarios

# Cria um Blueprint para as rotas de usuários
usuario_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")

  #Rota CREATE (POST)
@usuario_bp.route("/", methods=["POST"])
@jwt_required()
def criar_usuario():
    data = request.get_json()

    novo = Usuarios(
        nome=data.get("nome"),
        email=data.get("email"),
        senha=data.get("senha")
    )
    db.session.add(novo)
    db.session.commit()

    return jsonify({
        "message": "Usuário criado com sucesso",
        "usuario": novo.as_dict()
    }), 201

 #Rota READ(GET)
@usuario_bp.route("/", methods=["GET"])
@jwt_required()
def listar_usuarios():
    usuarios = Usuarios.query.all()

    return jsonify({
        "usuarios": [u.as_dict() for u in usuarios ], # Converte cada usuário para um dicionário usando o método as_dict()
        "total": len(usuarios) # Retorna o total de usuários encontrados
    })

#Rota read (Por id)

@usuario_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def buscar_usuario(id):
    usuario = Usuarios.query.get_or_404(id) # Busca o usuário pelo ID ou retorna 404 se não encontrado
    return jsonify(usuario.as_dict())


#rota Uptade
@usuario_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar_usuario(id):
    usuario = Usuarios.query.get_or_404(id) 
    data = request.get_json()
     
    for key, value in data.items(): # Itera sobre os dados fornecidos para atualização
        setattr(usuario, key, value )  # Atualiza os atributos do usuário com os dados fornecidos

    db.session.commit()

    return jsonify({
        "message": "Atualizado com sucesso",
        "usuario": usuario.as_dict()
    })


#Rota (delete)

@usuario_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def deletar_usuario(id):
    usuario = Usuarios.query.get_or_404(id) # Busca o usuário pelo ID ou retorna 404 se não encontrado

    db.session.delete(usuario) 
    db.session.commit()

    return jsonify({"message": "Usuário deletado com sucesso"})