from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///contacts.db"
db = SQLAlchemy(app)

# Creando modelo de base de datos
class Contacto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(11), nullable=False)

    def serializar(self):
        return {
        'id': self.id,
        'name':self.name,
        'email':self.email,
        'phone':self.phone
        }
    
    # Creando las tablas en la base de datos
    with app.app_context():
        db.create_all() 


