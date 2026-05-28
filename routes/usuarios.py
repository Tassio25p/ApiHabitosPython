from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash
from db import db
from Models.usuarios import Usuarios

usuario_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@usuario_bp.route("", methods=["GET"])
@jwt_required()
def listar_usuarios():
    """
    Lista usuários cadastrados com paginação e filtros opcionais
    ---
    tags:
      - Usuários
    security:
      - Bearer: []
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        example: 1
        description: Número da página desejada
      - name: per_page
        in: query
        type: integer
        required: false
        example: 5
        description: Quantidade de registros por página
      - name: nome
        in: query
        type: string
        required: false
        example: Tassio
        description: Filtro opcional pelo nome do usuário
      - name: email
        in: query
        type: string
        required: false
        example: tassio@email.com
        description: Filtro opcional pelo email do usuário
    responses:
      200:
        description: Lista de usuários retornada com sucesso
      401:
        description: Token JWT ausente ou inválido
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    nome = request.args.get("nome")
    email = request.args.get("email")

    if per_page > 20:
        per_page = 20

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


@usuario_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def buscar_usuario(id):
    """
    Busca um usuário pelo ID
    ---
    tags:
      - Usuários
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        example: 1
        description: ID do usuário
    responses:
      200:
        description: Usuário encontrado com sucesso
      401:
        description: Token JWT ausente ou inválido
      404:
        description: Usuário não encontrado
    """
    usuario = Usuarios.query.get_or_404(id)
    return jsonify(usuario.as_dict()), 200


@usuario_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar_usuario(id):
    """
    Atualiza os dados de um usuário
    ---
    tags:
      - Usuários
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        example: 1
        description: ID do usuário
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: Tassio Atualizado
            email:
              type: string
              example: tassio.novo@email.com
            senha:
              type: string
              example: "123456"
              description: Nova senha com no mínimo 6 caracteres
    responses:
      200:
        description: Usuário atualizado com sucesso
      400:
        description: Dados inválidos, email em uso ou senha menor que 6 caracteres
      401:
        description: Token JWT ausente ou inválido
      404:
        description: Usuário não encontrado
    """
    usuario = Usuarios.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({"message": "Envie os dados em formato JSON."}), 400

    if "nome" in data:
        if not data["nome"]:
            return jsonify({"message": "O nome não pode ficar vazio."}), 400
        usuario.nome = data["nome"]

    if "email" in data:
        if not data["email"]:
            return jsonify({"message": "O email não pode ficar vazio."}), 400

        email_existente = Usuarios.query.filter(
            Usuarios.email == data["email"],
            Usuarios.id != id
        ).first()

        if email_existente:
            return jsonify({"message": "Este email já está em uso."}), 400

        usuario.email = data["email"]

    if "senha" in data:
        if len(data["senha"]) < 6:
            return jsonify({"message": "A senha deve ter no mínimo 6 caracteres."}), 400

        usuario.senha = generate_password_hash(data["senha"])

    db.session.commit()

    return jsonify({
        "message": "Usuário atualizado com sucesso.",
        "usuario": usuario.as_dict()
    }), 200


@usuario_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def deletar_usuario(id):
    """
    Deleta um usuário pelo ID
    ---
    tags:
      - Usuários
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        example: 1
        description: ID do usuário
    responses:
      200:
        description: Usuário deletado com sucesso
      401:
        description: Token JWT ausente ou inválido
      404:
        description: Usuário não encontrado
    """
    usuario = Usuarios.query.get_or_404(id)

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({"message": "Usuário deletado com sucesso."}), 200