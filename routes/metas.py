from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from db import db
from Models.metas import Metas

metas_bp = Blueprint("metas", __name__, url_prefix="/metas")


@metas_bp.route("", methods=["POST"])
@jwt_required()
def criar_meta():
    """
    Cria uma nova meta para o usuário autenticado
    ---
    tags:
      - Metas
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - descricao
            - objetivo
          properties:
            descricao:
              type: string
              example: Manter rotina de estudos por 30 dias
            objetivo:
              type: string
              example: "2026-06-30T23:59:00"
              description: Data objetivo no formato YYYY-MM-DDTHH:MM:SS
    responses:
      201:
        description: Meta criada com sucesso
      400:
        description: Dados inválidos, descrição obrigatória ou formato de data inválido
      401:
        description: Token JWT ausente ou inválido
    """
    data = request.get_json()
    usuario_id = get_jwt_identity()

    if not data:
        return jsonify({"message": "Envie os dados em formato JSON."}), 400

    descricao = data.get("descricao")
    objetivo = data.get("objetivo")

    if not descricao:
        return jsonify({"message": "A descrição da meta é obrigatória."}), 400

    if not objetivo:
        return jsonify({"message": "O objetivo/data da meta é obrigatório."}), 400

    try:
        objetivo_data = datetime.fromisoformat(objetivo)
    except ValueError:
        return jsonify({
            "message": "Formato de data inválido. Use: YYYY-MM-DDTHH:MM:SS"
        }), 400

    nova_meta = Metas(
        descricao=descricao,
        objetivo=objetivo_data,
        usuario_id=usuario_id
    )

    db.session.add(nova_meta)
    db.session.commit()

    return jsonify({
        "message": "Meta criada com sucesso.",
        "meta": nova_meta.as_dict()
    }), 201


@metas_bp.route("", methods=["GET"])
@jwt_required()
def listar_metas():
    """
    Lista as metas do usuário autenticado com paginação
    ---
    tags:
      - Metas
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
        description: Lista de metas retornada com sucesso
      401:
        description: Token JWT ausente ou inválido
    """
    usuario_id = get_jwt_identity()

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    if per_page > 20:
        per_page = 20

    paginacao = Metas.query.filter_by(usuario_id=usuario_id).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "metas": [m.as_dict() for m in paginacao.items],
        "pagina_atual": paginacao.page,
        "por_pagina": paginacao.per_page,
        "total_registros": paginacao.total,
        "total_paginas": paginacao.pages
    }), 200


@metas_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def buscar_meta(id):
    """
    Busca uma meta do usuário autenticado pelo ID
    ---
    tags:
      - Metas
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        example: 1
        description: ID da meta
    responses:
      200:
        description: Meta encontrada com sucesso
      401:
        description: Token JWT ausente ou inválido
      404:
        description: Meta não encontrada
    """
    usuario_id = get_jwt_identity()

    meta = Metas.query.filter_by(
        id=id,
        usuario_id=usuario_id
    ).first()

    if not meta:
        return jsonify({"message": "Meta não encontrada."}), 404

    return jsonify(meta.as_dict()), 200


@metas_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar_meta(id):
    """
    Atualiza uma meta do usuário autenticado
    ---
    tags:
      - Metas
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        example: 1
        description: ID da meta
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            descricao:
              type: string
              example: Manter o hábito por 60 dias
            objetivo:
              type: string
              example: "2026-07-30T23:59:00"
              description: Data objetivo no formato YYYY-MM-DDTHH:MM:SS
    responses:
      200:
        description: Meta atualizada com sucesso
      400:
        description: Dados inválidos, descrição vazia ou formato de data inválido
      401:
        description: Token JWT ausente ou inválido
      404:
        description: Meta não encontrada
    """
    usuario_id = get_jwt_identity()

    meta = Metas.query.filter_by(
        id=id,
        usuario_id=usuario_id
    ).first()

    if not meta:
        return jsonify({"message": "Meta não encontrada."}), 404

    data = request.get_json()

    if not data:
        return jsonify({"message": "Envie os dados em formato JSON."}), 400

    if "descricao" in data:
        if not data["descricao"]:
            return jsonify({"message": "A descrição não pode ficar vazia."}), 400
        meta.descricao = data["descricao"]

    if "objetivo" in data:
        try:
            meta.objetivo = datetime.fromisoformat(data["objetivo"])
        except ValueError:
            return jsonify({
                "message": "Formato de data inválido. Use: YYYY-MM-DDTHH:MM:SS"
            }), 400

    db.session.commit()

    return jsonify({
        "message": "Meta atualizada com sucesso.",
        "meta": meta.as_dict()
    }), 200


@metas_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def deletar_meta(id):
    """
    Deleta uma meta do usuário autenticado
    ---
    tags:
      - Metas
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        example: 1
        description: ID da meta
    responses:
      200:
        description: Meta deletada com sucesso
      401:
        description: Token JWT ausente ou inválido
      404:
        description: Meta não encontrada
    """
    usuario_id = get_jwt_identity()

    meta = Metas.query.filter_by(
        id=id,
        usuario_id=usuario_id
    ).first()

    if not meta:
        return jsonify({"message": "Meta não encontrada."}), 404

    db.session.delete(meta)
    db.session.commit()

    return jsonify({"message": "Meta deletada com sucesso."}), 200