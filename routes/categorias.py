from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from db import db
from Models.categorias import Categorias

categorias_bp = Blueprint('categorias', __name__)




#Rota CREATE (POST)
@categorias_bp.route('/categorias', methods=["POST"])
def criar_categoria():
    data = request.get_json()

    novo = Categorias(
        nome=data.get("nome")
    )

    db.session.add(novo)
    db.session.commit()

    return jsonify({
        "message": "Categoria criada com sucesso",
        "categoria": novo.as_dict()
    }), 201


#Rota READ (GET)
@categorias_bp.route('/categorias', methods=["GET"])
def listar_categorias():
    categorias = Categorias.query.all()

    return jsonify({
        "categorias": [c.as_dict() for c in categorias],
        "total": len(categorias)
    })


#Rota READ por ID
@categorias_bp.route('/categorias/<int:id>', methods=["GET"])
def buscar_categoria(id):
    categoria = Categorias.query.get_or_404(id)

    return jsonify(categoria.as_dict())


#Rota UPDATE (PUT)
@categorias_bp.route('/categorias/<int:id>', methods=["PUT"])
def atualizar_categoria(id):
    categoria = Categorias.query.get_or_404(id)
    data = request.get_json()

    for key, value in data.items():
        setattr(categoria, key, value)

    db.session.commit()

    return jsonify({
        "message": "Atualizado com sucesso",
        "categoria": categoria.as_dict()
    })


#Rota DELETE
@categorias_bp.route('/categorias/<int:id>', methods=["DELETE"])
def deletar_categoria(id):
    categoria = Categorias.query.get_or_404(id)

    db.session.delete(categoria)
    db.session.commit()

    return jsonify({
        "message": "Categoria deletada com sucesso"
    })