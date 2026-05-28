from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from db import db
from Models.registros import Registros_habitos
from Models.habitos import Habitos

registros_bp = Blueprint("registros", __name__, url_prefix="/registros")


@registros_bp.route("", methods=["POST"])
@jwt_required()
def criar_registro():
    """
    Cria um novo registro de hábito para o usuário autenticado
    ---
    tags:
      - Registros
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - habito_id
            - data
          properties:
            habito_id:
              type: integer
              example: 1
            data:
              type: string
              example: "2026-05-24T20:00:00"
              description: Data do registro no formato YYYY-MM-DDTHH:MM:SS
            concluido:
              type: boolean
              example: true
    responses:
      201:
        description: Registro criado com sucesso
      400:
        description: Dados inválidos, campos obrigatórios ausentes ou formato de data inválido
      401:
        description: Token JWT ausente ou inválido
      404:
        description: Hábito não encontrado
    """
    data = request.get_json()
    usuario_id = get_jwt_identity()

    if not data:
        return jsonify({"message": "Envie os dados em formato JSON."}), 400

    habito_id = data.get("habito_id")
    data_registro = data.get("data")
    concluido = data.get("concluido", False)

    if not habito_id:
        return jsonify({"message": "O ID do hábito é obrigatório."}), 400

    if not data_registro:
        return jsonify({"message": "A data do registro é obrigatória."}), 400

    habito = Habitos.query.filter_by(
        id=habito_id,
        usuario_id=usuario_id
    ).first()

    if not habito:
        return jsonify({"message": "Hábito não encontrado."}), 404

    if not isinstance(concluido, bool):
        return jsonify({"message": "O campo concluido deve ser true ou false."}), 400

    try:
        data_convertida = datetime.fromisoformat(data_registro)
    except ValueError:
        return jsonify({
            "message": "Formato de data inválido. Use: YYYY-MM-DDTHH:MM:SS"
        }), 400

    novo_registro = Registros_habitos(
        habito_id=habito_id,
        data=data_convertida,
        concluido=concluido
    )

    db.session.add(novo_registro)
    db.session.commit()

    return jsonify({
        "message": "Registro criado com sucesso.",
        "registro": novo_registro.as_dict()
    }), 201


@registros_bp.route("", methods=["GET"])
@jwt_required()
def listar_registros():
    """
    Lista os registros de hábitos do usuário autenticado com paginação
    ---
    tags:
      - Registros
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
        description: Lista de registros retornada com sucesso
      401:
        description: Token JWT ausente ou inválido
    """
    usuario_id = get_jwt_identity()

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    if per_page > 20:
        per_page = 20

    paginacao = Registros_habitos.query.join(Habitos).filter(
        Habitos.usuario_id == usuario_id
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "registros": [r.as_dict() for r in paginacao.items],
        "pagina_atual": paginacao.page,
        "por_pagina": paginacao.per_page,
        "total_registros": paginacao.total,
        "total_paginas": paginacao.pages
    }), 200


@registros_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def buscar_registro(id):
    """
    Busca um registro de hábito do usuário autenticado pelo ID
    ---
    tags:
      - Registros
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        example: 1
        description: ID do registro
    responses:
      200:
        description: Registro encontrado com sucesso
      401:
        description: Token JWT ausente ou inválido
      404:
        description: Registro não encontrado
    """
    usuario_id = get_jwt_identity()

    registro = Registros_habitos.query.join(Habitos).filter(
        Registros_habitos.id == id,
        Habitos.usuario_id == usuario_id
    ).first()

    if not registro:
        return jsonify({"message": "Registro não encontrado."}), 404

    return jsonify(registro.as_dict()), 200


@registros_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar_registro(id):
    """
    Atualiza um registro de hábito do usuário autenticado
    ---
    tags:
      - Registros
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        example: 1
        description: ID do registro
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            habito_id:
              type: integer
              example: 1
            data:
              type: string
              example: "2026-05-25T20:00:00"
              description: Data do registro no formato YYYY-MM-DDTHH:MM:SS
            concluido:
              type: boolean
              example: false
    responses:
      200:
        description: Registro atualizado com sucesso
      400:
        description: Dados inválidos ou formato de data inválido
      401:
        description: Token JWT ausente ou inválido
      404:
        description: Registro ou hábito não encontrado
    """
    usuario_id = get_jwt_identity()

    registro = Registros_habitos.query.join(Habitos).filter(
        Registros_habitos.id == id,
        Habitos.usuario_id == usuario_id
    ).first()

    if not registro:
        return jsonify({"message": "Registro não encontrado."}), 404

    data = request.get_json()

    if not data:
        return jsonify({"message": "Envie os dados em formato JSON."}), 400

    if "habito_id" in data:
        habito = Habitos.query.filter_by(
            id=data["habito_id"],
            usuario_id=usuario_id
        ).first()

        if not habito:
            return jsonify({"message": "Hábito não encontrado."}), 404

        registro.habito_id = data["habito_id"]

    if "data" in data:
        try:
            registro.data = datetime.fromisoformat(data["data"])
        except ValueError:
            return jsonify({
                "message": "Formato de data inválido. Use: YYYY-MM-DDTHH:MM:SS"
            }), 400

    if "concluido" in data:
        if not isinstance(data["concluido"], bool):
            return jsonify({"message": "O campo concluido deve ser true ou false."}), 400

        registro.concluido = data["concluido"]

    db.session.commit()

    return jsonify({
        "message": "Registro atualizado com sucesso.",
        "registro": registro.as_dict()
    }), 200


@registros_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def deletar_registro(id):
    """
    Deleta um registro de hábito do usuário autenticado
    ---
    tags:
      - Registros
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        example: 1
        description: ID do registro
    responses:
      200:
        description: Registro deletado com sucesso
      401:
        description: Token JWT ausente ou inválido
      404:
        description: Registro não encontrado
    """
    usuario_id = get_jwt_identity()

    registro = Registros_habitos.query.join(Habitos).filter(
        Registros_habitos.id == id,
        Habitos.usuario_id == usuario_id
    ).first()

    if not registro:
        return jsonify({"message": "Registro não encontrado."}), 404

    db.session.delete(registro)
    db.session.commit()

    return jsonify({"message": "Registro deletado com sucesso."}), 200