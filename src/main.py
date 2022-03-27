"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os, requests
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Vehicle

#from models import Person

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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# @app.route('/people')
# def get_people():
#     req = requests.get("https://www.swapi.tech/api")    
#     return("Hablame")

BASE_URL = "https://www.swapi.tech/api/"

#Endpoints para la liste de personajes, planetas y vehiculos:

@app.route('/people', methods=["GET"])
def handle_characters():
    characters = Character.query.all()
    return jsonify(list(map(
        lambda character: character.shortalize(),
        characters
    ))), 200

@app.route('/planets', methods=["GET"])
def handle_planets():
    planets = Planet.query.all()
    return jsonify(list(map(
        lambda planet: planet.shortalize(),
        planets
    ))), 200

@app.route('/vehicles', methods=["GET"])
def handle_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify(list(map(
        lambda vehicle: vehicle.shortalize(),
        vehicles
    ))), 200

#Endpoints para personaje, planeta o vehiculo individual y detallado:

@app.route('/people/<int:id>')
def handle_one_character(id):
    character = Character.query.get(id)
    if character is None:
        return jsonify({
            "msg": "not found"
        }), 404
    return jsonify(character.serialize()), 200


@app.route('/planets/<int:id>')
def handle_one_planet(id):
    planet = Planet.query.get(id)
    if planet is None:
        return jsonify({
            "msg": "not found"
        }), 404
    return jsonify(planet.serialize()), 200

@app.route('/vehicles/<int:id>')
def handle_one_vehicle(id):
    vehicle = Vehicle.query.get(id)
    if vehicle is None:
        return jsonify({
            "msg": "not found"
        }), 404
    return jsonify(vehicle.serialize()), 200

#Endpoint que ya no uso, para obtener la lista de personajes y ademas crear los personajes 
#mediante endpoint para llenar la db, que se cambio por el script populate_db
# @app.route('/characters', methods=["GET", "POST"])
# def handle_characters():
#     if request.method == "GET":
#         characters = Character.query.all()
#         return jsonify(list(map(
#             lambda character: character.shortalize(),
#             characters
#         ))), 200
#     else:
#         body = request.json
#         character = Character.create(
#             name=body['name'],
#             eye_color=body['eye_color']
#         )
#         dictionary = character.serialize()
#         return jsonify(dictionary), 201


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

with app.app_context():
    from populate_db import populate_db