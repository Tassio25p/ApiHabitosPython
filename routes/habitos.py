from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from db import db
from Models.habitos import Habitos

habitos_bp = Blueprint('habitos', __name__, url_prefix='/habitos')

#Habitos
#Rota CREATE (POST)
@habitos_bp.route('', methods=["POST"])
@jwt_required() # Exige autenticação JWT para acessar esta rota
def criar_habito():
    data = request.get_json()
    nome = data.get("nome")
    descricao = data.get("descricao")
    usuario_id = data.get("usuario_id")

    if not nome or nome.strip() == "": # Verifica se o nome do hábito é fornecido e não é apenas espaços em branco
        return jsonify({"message": "O nome do hábito é obrigatório."}), 400

    if not descricao or descricao.strip() == "": # Verifica se a descrição do hábito é fornecida e não é apenas espaços em branco
        return jsonify({"message": "A descrição do hábito é obrigatória."}), 400
    
    if not usuario_id: # Verifica se o ID do usuário associado ao hábito é fornecido
        return jsonify({"message": "O ID do usuário associado ao hábito é obrigatório."}), 400


    novo = Habitos(
        nome=nome,
        descricao=descricao,
        usuario_id=usuario_id
    )
   
    db.session.add(novo)
    db.session.commit()

    return jsonify({
        "message": "Hábito criado com sucesso",
        "habito": novo.as_dict()
    }), 201


#Rota READ (GET)
@habitos_bp.route('', methods=["GET"])
@jwt_required() # Exige autenticação JWT para acessar esta rota
def listar_habitos():
    page = request.args.get("page", 1, type=int) # Obtém o número da página a partir dos parâmetros da URL, com valor padrão 1
    per_page = request.args.get("per_page", 5, type=int) # obtem o número de itens por página a partir dos parâmetros da URL, com valor padrão 5

    paginacao = Habitos.query.paginate( # Realiza a paginação dos resultados da consulta de hábitos
        page=page,
        per_page=per_page,
        error_out=False # Impede que a função lance um erro 404 se a página solicit
    )
    habitos = paginacao.items # Obtém os hábitos da página atual a partir do objeto de paginação

    return jsonify({
    "habitos": [h.as_dict() for h in habitos], # Converte cada hábito para um dicionário usando o método as_dict() e retorna como uma lista
    "pagina_atual": paginacao.page, # Retorna o número da página atual
    "por_pagina": paginacao.per_page, # Retorna o número de itens
    "total_registros": paginacao.total, # Retorna o total de registros disponíveis
    "total_paginas": paginacao.pages # Retorna o total de páginas disponíveis

    })


#Rota READ por ID
@habitos_bp.route('/<int:id>', methods=["GET"])
@jwt_required() # Exige autenticação JWT para acessar esta rota
def buscar_habito(id):
   
    habito = Habitos.query.get_or_404(id) # Busca o hábito pelo ID ou retorna 404 se não encontrado

    return jsonify(habito.as_dict()) # Retorna os detalhes do hábito encontrado como um dicionário usando o método as_dict()


#Rota UPDATE (PUT)
@habitos_bp.route('/<int:id>', methods=["PUT"])
@jwt_required() # Exige autenticação JWT para acessar esta rota
def atualizar_habito(id):
    habito = Habitos.query.get_or_404(id) # Busca o hábito pelo ID ou retorna 404 se não encontrado
    data = request.get_json() # Obtém os dados fornecidos para atualização a partir do corpo da requisição

    for key, value in data.items(): # Itera sobre os dados fornecidos para atualização
        if "nome" in data:
            habito.nome = data["nome"] # Atualiza o nome do hábito se fornecido
        if "descricao" in data:
            habito.descricao = data["descricao"] # Atualiza a descrição do hábito se fornecida
        if "usuario_id" in data:
            habito.usuario_id = data["usuario_id"] # Atualiza o ID do usuário associado ao hábito se fornecido


    db.session.commit()

    return jsonify({
        "message": "Atualizado com sucesso",
        "habito": habito.as_dict()
    })


#Rota DELETE
@habitos_bp.route('/<int:id>', methods=["DELETE"])
@jwt_required() # Exige autenticação JWT para acessar esta rota
def deletar_habito(id):
    habito = Habitos.query.get_or_404(id) # Busca o hábito pelo ID ou retorna 404 se não encontrado

    db.session.delete(habito)
    db.session.commit()

    return jsonify({
        "message": "Hábito deletado com sucesso"
    })

