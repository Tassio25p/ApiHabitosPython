from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from db import db
from Models.usuarios import Usuarios

# Cria um Blueprint para as rotas de usuários
usuario_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")

 #Rota READ(GET)
@usuario_bp.route("", methods=["GET"])
@jwt_required()
def listar_usuarios():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    nome = request.args.get("nome")
    email = request.args.get("email")
    query = Usuarios.query

    if nome:
        query = query.filter(Usuarios.nome.ilike(f"%{nome}%"))

    if email:
        query = query.filter(Usuarios.email.ilike(f"%{email}%"))

    paginacao = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "usuarios": [u.as_dict() for u in paginacao.items],
        "pagina_atual": paginacao.page,
        "por_pagina": paginacao.per_page,
        "total_registros": paginacao.total,
        "total_paginas": paginacao.pages
    }), 200
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
        if "nome" in data:
            usuario.nome = data["nome"] # Atualiza o nome do usuário se fornecido
        if "email" in data:
            usuario.email = data["email"] # Atualiza o email do usuário se fornecido
        if "senha" in data:
            usuario.senha = data["senha"] # Atualiza a senha do usuário se fornecida

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
    return jsonify({
        "message": "Usuário deletado com sucesso"
    })
