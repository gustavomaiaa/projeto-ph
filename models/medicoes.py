from datetime import datetime
from app import db  # ajuste o import para o seu projeto

class Medicao(db.Model):
    __tablename__ = 'medicoes'  # confirma o nome da tabela no banco

    id = db.Column(db.Integer, primary_key=True)
    ph = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "ph": self.ph,
            "data": self.data.isoformat()
        }
