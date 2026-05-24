from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime

from db import db
from Models.metas import Metas
from Models.usuarios import Usuarios


metas_bp = Blueprint("metas", __name__, url_prefix="/metas")

@metas_bp.route("", methods=["POST"])
@jwt_required()
def criar_meta():
    data = request.get_json()  
    
    descricao = data.get("descricao")
    objetivo = data.get("objetivo")
    usuario_id = data.get("usuario_id")

    if not descricao:
        return jsonify({"message": "A descrição da meta é obrigatória."}), 400

    if not objetivo:
        return jsonify({"message": "O objetivo/data da meta é obrigatório."}), 400

    if not usuario_id:
        return jsonify({"message": "O ID do usuário é obrigatório."}), 400

    usuario = Usuarios.query.get(usuario_id) 

    if not usuario:
        return jsonify({"message": "Usuário não encontrado."}), 404

    try: # pegando erro no formt da data
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
        "message": "Meta criada com sucesso!",
        "meta": nova_meta.as_dict()
    }), 201


@metas_bp.route("", methods=["GET"])
@jwt_required()
def listar_metas():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    if per_page > 20:
        per_page = 20

    paginacao = Metas.query.paginate(
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


# READ POR ID
@metas_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def buscar_meta(id):
    meta = Metas.query.get_or_404(id)

    return jsonify(meta.as_dict()), 200


# UPDATE
@metas_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar_meta(id):
    meta = Metas.query.get_or_404(id)
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
        "message": "Meta atualizada com sucesso!",
        "meta": meta.as_dict()
    }), 200


# DELETE
@metas_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def deletar_meta(id):
    meta = Metas.query.get_or_404(id)

    db.session.delete(meta)
    db.session.commit()

    return jsonify({
        "message": "Meta deletada com sucesso!"
    }), 200