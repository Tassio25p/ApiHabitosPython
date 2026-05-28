from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from Models.habitos import Habitos

habitos_bp = Blueprint("habitos", __name__, url_prefix="/habitos")


@habitos_bp.route("", methods=["POST"])
@jwt_required()
def criar_habito():
    """
    Cria um novo hábito para o usuário autenticado
    ---
    tags:
      - Hábitos
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
              example: Beber água
            descricao:
              type: string
              example: Beber pelo menos 2 litros de água por dia
    responses:
      201:
        description: Hábito criado com sucesso
      400:
        description: Dados inválidos, nome obrigatório ou hábito já existente
      401:
        description: Token JWT ausente ou inválido
    """
    data = request.get_json()
    usuario_id = get_jwt_identity()

    if not data:
        return jsonify({"message": "Envie os dados em formato JSON."}), 400

    nome = data.get("nome")
    descricao = data.get("descricao", "")

    if not nome:
        return jsonify({"message": "O nome do hábito é obrigatório."}), 400

    habito_existente = Habitos.query.filter_by(
        nome=nome,
        usuario_id=usuario_id
    ).first()

    if habito_existente:
        return jsonify({"message": "Você já possui um hábito com este nome."}), 400

    novo_habito = Habitos(
        nome=nome,
        descricao=descricao,
        usuario_id=usuario_id
    )

    db.session.add(novo_habito)
    db.session.commit()

    return jsonify({
        "message": "Hábito criado com sucesso.",
        "habito": novo_habito.as_dict()
    }), 201


@habitos_bp.route("", methods=["GET"])
@jwt_required()
def listar_habitos():
    """
    Lista os hábitos do usuário autenticado com paginação
    ---
    tags:
      - Hábitos
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
        description: Lista de hábitos retornada com sucesso
      401:
        description: Token JWT ausente ou inválido
    """
    usuario_id = get_jwt_identity()

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    if per_page > 20:
        per_page = 20

    paginacao = Habitos.query.filter_by(usuario_id=usuario_id).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "habitos": [h.as_dict() for h in paginacao.items],
        "pagina_atual": paginacao.page,
        "por_pagina": paginacao.per_page,
        "total_registros": paginacao.total,
        "total_paginas": paginacao.pages
    }), 200


@habitos_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def buscar_habito(id):
    """
    Busca um hábito do usuário autenticado pelo ID
    ---
    tags:
      - Hábitos
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        example: 1
        description: ID do hábito
    responses:
      200:
        description: Hábito encontrado com sucesso
      401:
        description: Token JWT ausente ou inválido
      404:
        description: Hábito não encontrado
    """
    usuario_id = get_jwt_identity()

    habito = Habitos.query.filter_by(
        id=id,
        usuario_id=usuario_id
    ).first()

    if not habito:
        return jsonify({"message": "Hábito não encontrado."}), 404

    return jsonify(habito.as_dict()), 200


@habitos_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar_habito(id):
    """
    Atualiza um hábito do usuário autenticado
    ---
    tags:
      - Hábitos
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        example: 1
        description: ID do hábito
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: Beber água atualizado
            descricao:
              type: string
              example: Beber 3 litros de água por dia
    responses:
      200:
        description: Hábito atualizado com sucesso
      400:
        description: Dados inválidos ou nome vazio
      401:
        description: Token JWT ausente ou inválido
      404:
        description: Hábito não encontrado
    """
    usuario_id = get_jwt_identity()

    habito = Habitos.query.filter_by(
        id=id,
        usuario_id=usuario_id
    ).first()

    if not habito:
        return jsonify({"message": "Hábito não encontrado."}), 404

    data = request.get_json()

    if not data:
        return jsonify({"message": "Envie os dados em formato JSON."}), 400

    if "nome" in data:
        if not data["nome"]:
            return jsonify({"message": "O nome do hábito não pode ficar vazio."}), 400
        habito.nome = data["nome"]

    if "descricao" in data:
        habito.descricao = data["descricao"]

    db.session.commit()

    return jsonify({
        "message": "Hábito atualizado com sucesso.",
        "habito": habito.as_dict()
    }), 200


@habitos_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def deletar_habito(id):
    """
    Deleta um hábito do usuário autenticado
    ---
    tags:
      - Hábitos
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        example: 1
        description: ID do hábito
    responses:
      200:
        description: Hábito deletado com sucesso
      401:
        description: Token JWT ausente ou inválido
      404:
        description: Hábito não encontrado
    """
    usuario_id = get_jwt_identity()

    habito = Habitos.query.filter_by(
        id=id,
        usuario_id=usuario_id
    ).first()

    if not habito:
        return jsonify({"message": "Hábito não encontrado."}), 404

    db.session.delete(habito)
    db.session.commit()

    return jsonify({"message": "Hábito deletado com sucesso."}), 200