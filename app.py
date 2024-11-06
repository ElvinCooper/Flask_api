from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///datos.db"
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


# Creando rutas o endpoints        
@app.route('/contact', methods=['GET'])
def get_contacts():
    contacts = Contacto.query.all()
    return jsonify({'contatcs': [contact.serializar() for contact in contacts]})
    db.session.close()

@app.route('/insertar', methods=['POST'])
def create_contact():
    data = request.get_json()    
    mi_contacto = Contacto(name=data['name'], email=data['email'], phone=data['phone'])
    db.session.add(mi_contacto)
    db.session.commit()
    return jsonify({'mensaje':'El contacto ha sido creado con exito', 'contacto': mi_contacto.serializar()}), 201
    

@app.route('/contact/<int:id>', methods=['GET'])
def get_contact(id):
    contacto = Contacto.query.get(id)
    if not contacto:
        return jsonify({'mensaje':'el contacto no existe'}), 404
    return jsonify({'mensaje':'El contacto ha sido creado con exito',
                    'contacto': contacto.serializar()}), 201


@app.route('/contact/<int:id>', methods=['PUT', 'PATCH'])
def update_contact(id):
    contacto = Contacto.query.get_or_404(id)
    data = request.get_json()

    if 'name' in data:
        contacto.name = data['name']
    if 'email' in data:
        contacto.email = data['email']
    if 'phone' in data:
        contacto.phone = data['phone']

    # guardando los cambios en la base de datos
    db.session.commit()
    return jsonify({'mensaje':'El contacto ha sido actualizado con exito','contacto': contacto.serializar()}), 201


@app.route('/contact/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contacto =  Contacto.query.get(id)
    if contacto:
        db.session.delete(contacto)
        db.session.commit()
        return jsonify({'mensaje':'Contacto eliminado con exito','contacto': contacto.serializar()}), 201
    return jsonify({'mensaje':'El contacto no existe'}), 404


