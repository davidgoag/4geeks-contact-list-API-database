"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Contact
#from models import Person
import json 

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/contact/all', methods=['GET'])
def get_contacts():

    contact_query = Contact.query.all()
    contacts = list(map(lambda contact: contact.serialize(), contact_query))

    return jsonify(contacts)

@app.route('/contact', methods=['POST'])
def add_contact():

    data = json.loads(request.data)
    
    contact = Contact.query.filter_by(email=data['email']).first()

    if contact is None:
        new_contact = Contact(**data)
        db.session.add(new_contact)
        db.session.commit()

        contact_query = Contact.query.all()
        contacts = list(map(lambda contact: contact.serialize(), contact_query))
        
        res = {
            "contacts": contacts,
            "message": "ok",
        } 

        return jsonify(res), 200

    return jsonify({"message": f"Email {data['email']} already exists as a contact"}), 400

    
    
@app.route('/contact/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    contact = Contact.query.get(contact_id)
    if contact is None:
        return jsonify({"message": f"Contact {contact_id} was not found"}), 400
    db.session.delete(contact)
    db.session.commit()

    contact_query = Contact.query.all()
    contacts = list(map(lambda contact: contact.serialize(), contact_query))
        
    res = {
        "contacts": contacts,
        "message": f"Contact {contact_id} deleted successfully",
    }

    return jsonify(res), 200

@app.route('/contact/<int:contact_id>', methods=['PUT'])
def edit_contact(contact_id):
    data = json.loads(request.data)
    contact = Contact.query.get(contact_id)
    if contact is None:
        return jsonify({"message": f"Contact {contact_id} was not found"}), 400
    
    if "full_name" in data:
        contact.full_name  = data["full_name"]
    if "adress" in data:
        contact.adress  = data["adress"]
    if "phone" in data:
        contact.phone  = data["phone"]
    if "email" in data:
        contact.email  = data["email"]

    db.session.commit()

    contact_query = Contact.query.all()
    contacts = list(map(lambda contact: contact.serialize(), contact_query))

    res = {
        "message": f"Contact {contact_id} updated successfully",
        "contacts": contacts,
    }

    return jsonify(res), 200
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
