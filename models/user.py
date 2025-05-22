from extensions import db
import uuid

class User(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.Text, nullable=False) 
    role = db.Column(db.String(20), default='user')
    
    nome = db.Column(db.String(100))  
    data_nascimento = db.Column(db.Date, nullable=False)  

    def __repr__(self):
        return f"<User {self.username}>"
