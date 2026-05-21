from db import db

class Registros_habitos(db.Model): 
     __tablename__ ="registros_habitos"

     id = db.Column(db.Integer,primary_key=True,autoincrement=True)
     habito_id = db.Column(db.Integer, db.ForeignKey('habitos.id'),nullable=False)
     data = db.Column(db.DateTime,nullable=False)
     concluido = db.Column(db.Boolean, default=False)
     
     def as_dict(self):
        return {
            "id": self.id,
            "habitos_id": self.habito_id,
            "data": self.data,
            "concluido": self.concluido
        }