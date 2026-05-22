from db import db


class Usuarios(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nome = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(50), unique=True,nullable=False)
    data_criacao = db.Column(db.DateTime, server_default=db.func.now())
    senha = db.Column(db.String(255),nullable=False)

    def as_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "data_criacao": self.data_criacao.isoformat() if self.data_criacao else None,
        }