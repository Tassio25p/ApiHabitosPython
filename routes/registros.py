from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime

from db import db
from Models.registros import Registros_habitos
from Models.habitos import Habitos


registros_bp = Blueprint("registros", __name__, url_prefix="/registros")


# CREATE
@registros_bp.route("", methods=["POST"])
@jwt_required()
def criar_registro():
    data = request.get_json()

    habito_id = data.get("habito_id")
    data_registro = data.get("data")
    concluido = data.get("concluido", False)

    if not habito_id:
        return jsonify({"message": "O ID do hábito é obrigatório."}), 400

    if not data_registro:
        return jsonify({"message": "A data do registro é obrigatória."}), 400

    habito = Habitos.query.get(habito_id)

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
        "message": "Registro criado com sucesso!",
        "registro": novo_registro.as_dict()
    }), 201


# READ TODOS COM PAGINAÇÃO
@registros_bp.route("", methods=["GET"])
@jwt_required()
def listar_registros():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    if per_page > 20:
        per_page = 20

    paginacao = Registros_habitos.query.paginate(
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


# READ POR ID
@registros_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def buscar_registro(id):
    registro = Registros_habitos.query.get_or_404(id)

    return jsonify(registro.as_dict()), 200


# UPDATE
@registros_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar_registro(id):
    registro = Registros_habitos.query.get_or_404(id)
    data = request.get_json()
    
    if "habito_id" in data:
        habito = Habitos.query.get(data["habito_id"])

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
        "message": "Registro atualizado com sucesso!",
        "registro": registro.as_dict()
    }), 200


# DELETE
@registros_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def deletar_registro(id):
    registro = Registros_habitos.query.get_or_404(id)

    db.session.delete(registro)
    db.session.commit()

    return jsonify({
        "message": "Registro deletado com sucesso!"
    }), 200