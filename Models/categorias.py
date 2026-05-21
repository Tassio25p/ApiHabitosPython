from db import db

class Categorias(db.Model):
     __tablename__ = "categorias"

     id = db.Column(db.Integer, primary_key=True,autoincrement=True)
     nome =  db.Column(db.String(100),nullable=False)

     def as_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            }