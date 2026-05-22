from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from db import db
from Models.registros import Registros_habitos


registros_bp = Blueprint('registros', __name__, url_prefix='/registros')


#Rota CREATE (POST)
@registros_bp.route('/', methods=["POST"])
def criar_registro():
    data = request.get_json()

    novo = Registros_habitos(
        habito_id=data.get("habito_id"),
        data=data.get("data"),
        concluido=data.get("concluido")

    )

    db.session.add(novo)
    db.session.commit()

    return jsonify({
        "message": "Registro criado com sucesso",
        "registro": novo.as_dict()
    }), 201


#Rota READ (GET)
@registros_bp.route('/', methods=["GET"])
def listar_registros():
    registros = Registros_habitos.query.all()

    return jsonify({
        "registros": [r.as_dict() for r in registros],
        "total": len(registros)
    })


#Rota READ por ID
@registros_bp.route('/<int:id>', methods=["GET"])
def buscar_registro(id):
    registro = Registros_habitos.query.get_or_404(id)

    return jsonify(registro.as_dict())


#Rota UPDATE (PUT)
@registros_bp.route('/<int:id>', methods=["PUT"])
def atualizar_registro(id):
  
    registro = Registros_habitos.query.get_or_404(id)
    data = request.get_json()

    for key, value in data.items():
        setattr(registro, key, value)

    db.session.commit()

    return jsonify({
        "message": "Atualizado com sucesso",
        "registro": registro.as_dict()
    })


#Rota DELETE
@registros_bp.route('/<int:id>', methods=["DELETE"])
def deletar_registro(id):
    registro = Registros_habitos.query.get_or_404(id)

    db.session.delete(registro)
    db.session.commit()

    return jsonify({
        "message": "Registro deletado com sucesso"
})