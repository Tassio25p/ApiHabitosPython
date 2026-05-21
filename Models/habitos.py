from db import db

class Habitos(db.Model):
    __tablename__ = "habitos"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nome = db.Column(db.String(100),nullable=False)
    descricao = db.Column(db.String(255),nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'),nullable=False)

    def as_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "usuario_id": self.usuario_id
        }