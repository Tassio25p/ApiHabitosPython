from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from db import db
from Models.categorias import Categorias

categorias_bp = Blueprint('categorias', __name__, url_prefix='/categorias')

#Rota CREATE (POST)
@categorias_bp.route('', methods=["POST"])
@jwt_required() # Exige autenticação JWT para acessar esta rota
def criar_categoria():
    data = request.get_json()
    nome = data.get("nome")
    if not nome or nome.strip() == "": # Verifica se o nome da categoria é fornecido e não é apenas espaços em branco
        return jsonify({"message": "O nome da categoria é obrigatório."}), 400

    novo = Categorias(nome=nome) 
    db.session.add(novo)
    db.session.commit()

    return jsonify({
        "message": "Categoria criada com sucesso",
        "categoria": novo.as_dict()
    }), 201


#Rota READ (GET)
@categorias_bp.route('', methods=["GET"])
@jwt_required() # Exige autenticação JWT para acessar esta rota
def listar_categorias():
    page = request.args.get("page", 1, type=int) # Obtém o número da página a partir dos parâmetros da URL, com valor padrão 1
    per_page = request.args.get("per_page", 5, type=int) # Obtem o número de itens por página a partir dos parâmetros da URL, com valor padrão 5
     
    paginacao = Categorias.query.paginate( # Realiza a paginação dos resultados da consulta de categorias
        page=page,
        per_page=per_page,
        error_out=False # Impede que a função lance um erro 404 se a página solicitada estiver fora do intervalo, retornando uma página vazia em vez disso
    )
     
    return jsonify({
    "categorias": [c.as_dict() for c in paginacao.items],
    "pagina_atual": paginacao.page,
    "por_pagina": paginacao.per_page,
    "total_registros": paginacao.total,
    "total_paginas": paginacao.pages
    })


#Rota READ por ID
@categorias_bp.route('/<int:id>', methods=["GET"])
@jwt_required() # Exige autenticação JWT para acessar esta rota
def buscar_categoria(id):
    categoria = Categorias.query.get_or_404(id)

    return jsonify(categoria.as_dict())


#Rota UPDATE (PUT)
@categorias_bp.route('/<int:id>', methods=["PUT"])
@jwt_required() # Exige autenticação JWT para acessar esta rota
def atualizar_categoria(id):
    categoria = Categorias.query.get_or_404(id)
    data = request.get_json()

    for key, value in data.items():
        if "nome" in data:
            categoria.nome = data["nome"] # Atualiza o nome da categoria se fornecido

    db.session.commit()

    return jsonify({
        "message": "Atualizado com sucesso",
        "categoria": categoria.as_dict()
    })


#Rota DELETE
@categorias_bp.route('/<int:id>', methods=["DELETE"])
@jwt_required() # Exige autenticação JWT para acessar esta rota
def deletar_categoria(id):
    categoria = Categorias.query.get_or_404(id)

    db.session.delete(categoria)
    db.session.commit()

    return jsonify({
        "message": "Categoria deletada com sucesso"
    })