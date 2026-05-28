from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from Models.categorias import Categorias

categorias_bp = Blueprint("categorias", __name__, url_prefix="/categorias")


@categorias_bp.route("", methods=["POST"])
@jwt_required()
def criar_categoria():
    """
    Cria uma nova categoria para o usuário autenticado
    ---
    tags:
      - Categorias
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - nome
          properties:
            nome:
              type: string
              example: Saúde
    responses:
      201:
        description: Categoria criada com sucesso
      400:
        description: Dados inválidos, nome obrigatório ou categoria já existente
      401:
        description: Token JWT ausente ou inválido
    """
    data = request.get_json()
    usuario_id = get_jwt_identity()

    if not data:
        return jsonify({"message": "Envie os dados em formato JSON."}), 400

    nome = data.get("nome")

    if not nome:
        return jsonify({"message": "O nome da categoria é obrigatório."}), 400

    categoria_existente = Categorias.query.filter_by(
        nome=nome,
        usuario_id=usuario_id
    ).first()

    if categoria_existente:
        return jsonify({"message": "Você já possui uma categoria com este nome."}), 400

    nova_categoria = Categorias(
        nome=nome,
        usuario_id=usuario_id
    )

    db.session.add(nova_categoria)
    db.session.commit()

    return jsonify({
        "message": "Categoria criada com sucesso.",
        "categoria": nova_categoria.as_dict()
    }), 201


@categorias_bp.route("", methods=["GET"])
@jwt_required()
def listar_categorias():
    """
    Lista as categorias do usuário autenticado com paginação
    ---
    tags:
      - Categorias
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
    responses:
      200:
        description: Lista de categorias retornada com sucesso
      401:
        description: Token JWT ausente ou inválido
    """
    usuario_id = get_jwt_identity()

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    if per_page > 20:
        per_page = 20

    paginacao = Categorias.query.filter_by(usuario_id=usuario_id).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "categorias": [c.as_dict() for c in paginacao.items],
        "pagina_atual": paginacao.page,
        "por_pagina": paginacao.per_page,
        "total_registros": paginacao.total,
        "total_paginas": paginacao.pages
    }), 200


@categorias_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def buscar_categoria(id):
    """
    Busca uma categoria do usuário autenticado pelo ID
    ---
    tags:
      - Categorias
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        example: 1
        description: ID da categoria
    responses:
      200:
        description: Categoria encontrada com sucesso
      401:
        description: Token JWT ausente ou inválido
      404:
        description: Categoria não encontrada
    """
    usuario_id = get_jwt_identity()

    categoria = Categorias.query.filter_by(
        id=id,
        usuario_id=usuario_id
    ).first()

    if not categoria:
        return jsonify({"message": "Categoria não encontrada."}), 404

    return jsonify(categoria.as_dict()), 200


@categorias_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar_categoria(id):
    """
    Atualiza uma categoria do usuário autenticado
    ---
    tags:
      - Categorias
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        example: 1
        description: ID da categoria
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: Saúde Atualizada
    responses:
      200:
        description: Categoria atualizada com sucesso
      400:
        description: Dados inválidos ou nome vazio
      401:
        description: Token JWT ausente ou inválido
      404:
        description: Categoria não encontrada
    """
    usuario_id = get_jwt_identity()

    categoria = Categorias.query.filter_by(
        id=id,
        usuario_id=usuario_id
    ).first()

    if not categoria:
        return jsonify({"message": "Categoria não encontrada."}), 404

    data = request.get_json()

    if not data:
        return jsonify({"message": "Envie os dados em formato JSON."}), 400

    if "nome" in data:
        if not data["nome"]:
            return jsonify({"message": "O nome da categoria não pode ficar vazio."}), 400

        categoria.nome = data["nome"]

    db.session.commit()

    return jsonify({
        "message": "Categoria atualizada com sucesso.",
        "categoria": categoria.as_dict()
    }), 200


@categorias_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def deletar_categoria(id):
    """
    Deleta uma categoria do usuário autenticado
    ---
    tags:
      - Categorias
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        example: 1
        description: ID da categoria
    responses:
      200:
        description: Categoria deletada com sucesso
      401:
        description: Token JWT ausente ou inválido
      404:
        description: Categoria não encontrada
    """
    usuario_id = get_jwt_identity()

    categoria = Categorias.query.filter_by(
        id=id,
        usuario_id=usuario_id
    ).first()

    if not categoria:
        return jsonify({"message": "Categoria não encontrada."}), 404

    db.session.delete(categoria)
    db.session.commit()

    return jsonify({"message": "Categoria deletada com sucesso."}), 200