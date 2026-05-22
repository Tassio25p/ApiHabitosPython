from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from db import db
from Models.habitos import Habitos

habitos_bp = Blueprint('habitos', __name__)

#Habitos
#Rota CREATE (POST)
@habitos_bp.route('/habitos', methods=["POST"])
def criar_habito():
    data = request.get_json()

    novo = Habitos(
        nome=data.get("nome"),
        descricao=data.get("descricao"),
        usuario_id=data.get("usuario_id")
   
    )
 
    db.session.add(novo)
    db.session.commit()

    return jsonify({
        "message": "Hábito criado com sucesso",
        "habito": novo.as_dict()
    }), 201


#Rota READ (GET)
@habitos_bp.route('/habitos', methods=["GET"])
def listar_habitos():
    habitos = Habitos.query.all()

    return jsonify({
        "habitos": [h.as_dict() for h in habitos], # Converte cada hábito para um dicionário usando o método as_dict()
        "total": len(habitos) # Retorna o total de hábitos encontrados
    })


#Rota READ por ID
@habitos_bp.route('/habitos/<int:id>', methods=["GET"])
def buscar_habito(id):
   
    habito = Habitos.query.get_or_404(id) # Busca o hábito pelo ID ou retorna 404 se não encontrado

    return jsonify(habito.as_dict()) # Retorna os detalhes do hábito encontrado como um dicionário usando o método as_dict()


#Rota UPDATE (PUT)
@habitos_bp.route('/habitos/<int:id>', methods=["PUT"])
def atualizar_habito(id):
    habito = Habitos.query.get_or_404(id) # Busca o hábito pelo ID ou retorna 404 se não encontrado
    data = request.get_json() # Obtém os dados fornecidos para atualização a partir do corpo da requisição

    for key, value in data.items(): # Itera sobre os dados fornecidos para atualização
        setattr(habito, key, value) # Atualiza os atributos do hábito com os dados fornecidos

    db.session.commit()

    return jsonify({
        "message": "Atualizado com sucesso",
        "habito": habito.as_dict()
    })


#Rota DELETE
@habitos_bp.route('/habitos/<int:id>', methods=["DELETE"])
def deletar_habito(id):
    habito = Habitos.query.get_or_404(id) # Busca o hábito pelo ID ou retorna 404 se não encontrado

    db.session.delete(habito)
    db.session.commit()

    return jsonify({
        "message": "Hábito deletado com sucesso"
    })

