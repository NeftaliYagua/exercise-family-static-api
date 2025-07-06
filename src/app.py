"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, abort
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")

@app.errorhandler(404)
def not_found_error(error):
    response = jsonify({
        "404": 404,
        "error": "Not Found",
        "message": error.description if
        error.description else "The requested URL was not found on the server."
    })
    response.status_code = 404
    return response

@app.errorhandler(500)
def not_found_error(error):
    response = jsonify({
        "500": 500,
        "error": "Internal Server Error",
        "message": error.description if error.description else "The server return a error."
    })
    response.status_code = 404
    return response

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {"hello": "world",
                     "family": members}
    return jsonify(response_body), 200

@app.route('/members', methods=['POST'])
def handle_crear():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {"hello": "creado con exito",
                     "family": members}
    return jsonify(response_body), 201

@app.route('/members/<int:member_id>', methods=['GET'])
def handle_leer(member_id):
    try:
        members = jackson_family.get_member(member_id)
        response_body = members
        return jsonify(response_body), 200
    except:
        abort(404)

@app.route('/members/<int:member_id>', methods=['POST'])
def handle_actualizar(member_id):
    try:
        members = jackson_family.get_member(member_id)
        response_body = members
        return jsonify(response_body), 204
    except:
        abort(404)

@app.route('/members/<int:member_id>', methods=['DELETE'])
def handle_eliminar(member_id):
    try:
        members = jackson_family.get_member(member_id)
        response_body = members
        return jsonify(response_body), 204
    except:
        abort(404)

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
