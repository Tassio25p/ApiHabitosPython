from db import db
from datetime import datetime

class Metas(db.Model): 
    __tablename__ = "metas"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    descricao = db.Column(db.String(255), nullable=False)
    objetivo = db.Column(db.DateTime, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    
    def as_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "objetivo": self.objetivo,
            "usuario_id": self.usuario_id
        }