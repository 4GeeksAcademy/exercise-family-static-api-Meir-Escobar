"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_all_members():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    print("obteniendo miembros")
    return jsonify(members), 200

#devolver un usuario
@app.route('/members/<int:member_id>', methods=['GET'])
def get_one_member(member_id):
    # llama a funcion de datos
    print("obteniendo un solo miembro")
    member = jackson_family.get_member(member_id)
    # comprueba
    if member is None:
        # devuelve un error 404
        return jsonify({"error": "Member not found"}), 404
    # devuelve el miembro si existe
    return jsonify(member), 200

# agregar un usuario
@app.route('/members', methods=['POST'])
def add_new_member():
    #leer los datos de la request
    member_data = request.get_json()
    print("datos recibidos:", member_data)
    #llamar a la funcion cone esos datos
    new_member = jackson_family.add_member(member_data)
    #imrimimos el nuevo miembro
    print("nuevo miembro añadido:", new_member)
    # Devolver el miembro con un código 200
    return jsonify(new_member), 200
    pass

# borrar un usuario
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_one_member(member_id):
    # Llamar a la función de la estructura de datos para intentar eliminar
    result = jackson_family.delete_member(member_id)
    print("resultado de la eliminación:", result)
    # Comprobar el resultado
    if result is None:
        #devolver un error 404
        return jsonify({"error": "Member not found"}), 404
    else:
        #devolver un mensaje de éxito
        return jsonify(result), 200


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
