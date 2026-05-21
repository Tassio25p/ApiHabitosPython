import pymysql
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from db import db

from Models.usuarios import Usuarios
from Models.categorias import Categorias
from Models.habitos import Habitos
from Models.metas import Metas
from Models.registros import Registros_habitos

# Cria a aplicação Flask
app = Flask(__name__)
app.config["SQLACHEMY_TRACK_NOTIFICATIONS"] = False 
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:Root#12345@localhost/Api'

db.init_app(app)
migrate = Migrate(app,db)


#rota principal
@app.route('/')
def BemVindo():
    return "Bem Vindo Usuario" # retorna mensagem

  #Rota CREATE (POST)

@app.route('/usuarios', methods=["POST"])
def criar_usuario():
    data = request.get_json()

    novo = Usuarios(
        nome=data.get("nome"),
        email=data.get("email")
    )

    db.session.add(novo)
    db.session.commit()

    return jsonify({
        "message": "Usuário criado com sucesso",
        "usuario": novo.as_dict()
    }), 201

 #Rota READ(GET)

@app.route('/usuarios', methods=["GET"])
def listar_usuarios():
    usuarios = Usuarios.query.all()

    return jsonify({
        "usuarios": [u.as_dict() for u in usuarios],
        "total": len(usuarios)
    })

#Rota read (Por id)

@app.route('/usuarios/<int:id>', methods=["GET"])
def buscar_usuario(id):
    usuario = Usuarios.query.get_or_404(id)

    return jsonify(usuario.as_dict())


#rota Uptade

@app.route('/usuarios/<int:id>', methods=["PUT"])
def atualizar_usuario(id):
    usuario = Usuarios.query.get_or_404(id)
    data = request.get_json()

    for key, value in data.items():
        setattr(usuario, key, value)

    db.session.commit()

    return jsonify({
        "message": "Atualizado com sucesso",
        "usuario": usuario.as_dict()
    })


#Rota (delete)

@app.route('/usuarios/<int:id>', methods=["DELETE"])
def deletar_usuario(id):
    usuario = Usuarios.query.get_or_404(id)

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({"message": "Usuário deletado com sucesso"})

#Habitos

#Rota CREATE (POST)
@app.route('/habitos', methods=["POST"])
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
@app.route('/habitos', methods=["GET"])
def listar_habitos():
    habitos = Habitos.query.all()

    return jsonify({
        "habitos": [h.as_dict() for h in habitos],
        "total": len(habitos)
    })


#Rota READ por ID
@app.route('/habitos/<int:id>', methods=["GET"])
def buscar_habito(id):
   
    habito = Habitos.query.get_or_404(id)

    return jsonify(habito.as_dict())


#Rota UPDATE (PUT)
@app.route('/habitos/<int:id>', methods=["PUT"])
def atualizar_habito(id):
    habito = Habitos.query.get_or_404(id)
    data = request.get_json()

    for key, value in data.items():
        setattr(habito, key, value)

    db.session.commit()

    return jsonify({
        "message": "Atualizado com sucesso",
        "habito": habito.as_dict()
    })


#Rota DELETE
@app.route('/habitos/<int:id>', methods=["DELETE"])
def deletar_habito(id):
    habito = Habitos.query.get_or_404(id)

    db.session.delete(habito)
    db.session.commit()

    return jsonify({
        "message": "Hábito deletado com sucesso"
    })

#Categorias

#Rota CREATE (POST)
@app.route('/categorias', methods=["POST"])
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
@app.route('/categorias', methods=["GET"])
def listar_categorias():
    categorias = Categorias.query.all()

    return jsonify({
        "categorias": [c.as_dict() for c in categorias],
        "total": len(categorias)
    })


#Rota READ por ID
@app.route('/categorias/<int:id>', methods=["GET"])
def buscar_categoria(id):
    categoria = Categorias.query.get_or_404(id)

    return jsonify(categoria.as_dict())


#Rota UPDATE (PUT)
@app.route('/categorias/<int:id>', methods=["PUT"])
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
@app.route('/categorias/<int:id>', methods=["DELETE"])
def deletar_categoria(id):
    categoria = Categorias.query.get_or_404(id)

    db.session.delete(categoria)
    db.session.commit()

    return jsonify({
        "message": "Categoria deletada com sucesso"
    })

#Registros

#Rota CREATE (POST)
@app.route('/registros', methods=["POST"])
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
@app.route('/registros', methods=["GET"])
def listar_registros():
    registros = Registros_habitos.query.all()

    return jsonify({
        "registros": [r.as_dict() for r in registros],
        "total": len(registros)
    })


#Rota READ por ID
@app.route('/registros/<int:id>', methods=["GET"])
def buscar_registro(id):
    registro = Registros_habitos.query.get_or_404(id)

    return jsonify(registro.as_dict())


#Rota UPDATE (PUT)
@app.route('/registros/<int:id>', methods=["PUT"])
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
@app.route('/registros/<int:id>', methods=["DELETE"])
def deletar_registro(id):
    registro = Registros_habitos.query.get_or_404(id)

    db.session.delete(registro)
    db.session.commit()

    return jsonify({
        "message": "Registro deletado com sucesso"
})