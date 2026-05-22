from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from db import db
from Models.registros import Registros_habitos


registros_bp = Blueprint('registros', __name__, url_prefix='/registros')


#Rota CREATE (POST)
@registros_bp.route('', methods=["POST"])
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
@registros_bp.route('', methods=["GET"])
def listar_registros():
    page = request.args.get("page", 1, type=int) # Obtém o número da página a partir dos parâmetros da URL, com valor padrão 1
    per_page = request.args.get("per_page", 5, type=int) # obtem o número de itens por página a partir dos parâmetros da URL, com valor padrão 5

    paginacao = Registros_habitos.query.paginate( # Realiza a paginação dos resultados da consulta de registros
        page=page,
        per_page=per_page,
        error_out=False # Impede que a função lance um erro 404 se a página solicitada estiver fora do intervalo, retornando uma página vazia em vez disso
    )
    registros = paginacao.itcategoriasems # Obtém os registros da página atual a partir do objeto

    return jsonify({
    "Registros": [r.as_dict() for r in registros], # Converte cada registro para um dicionário usando o método as_dict() e retorna como uma lista
    "pagina_atual": paginacao.page, # Retorna o número da página atual
    "por_pagina": paginacao.per_page, # Retorna o número de itens por página
    "total_registros": paginacao.total, # Retorna o total de registros disponíveis
    "total_paginas": paginacao.pages # Retorna o total de páginas disponíveis

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
        if "habito_id" in data:
            registro.habito_id = data["habito_id"] # Atualiza o ID do hábito associado ao registro se fornecido
        if "data" in data:
            registro.data = data["data"] # Atualiza a data do registro se fornecida
        if "concluido" in data:
            registro.concluido = data["concluido"] # Atualiza o status de conclusão do registro se fornecido

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