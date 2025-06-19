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
from models import db
from services import StarWarsService

app = Flask(__name__)
app.url_map.strict_slashes = False
service = StarWarsService()
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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






@app.route("/people", methods=["GET"])
def get_all_characters():
    characters = service.get_all_characters()
    return jsonify([c.serialize() for c in characters]), 200

@app.route("/people/<int:character_id>", methods=["GET"])
def get_character(character_id):
    character = service.get_character(character_id)
    if character:
        return jsonify(character.serialize()), 200
    return jsonify({"error": "Character not found"}), 404

@app.route("/planets", methods=["GET"])
def get_all_planets():
    planets = service.get_all_planets()
    return jsonify([p.serialize() for p in planets]), 200

@app.route("/planets/<int:planet_id>", methods=["GET"])
def get_planet(planet_id):
    planet = service.get_planet(planet_id)
    if planet:
        return jsonify(planet.serialize()), 200
    return jsonify({"error": "Planet not found"}), 404

@app.route("/vehicles", methods=["GET"])
def get_all_vehicles():
    vehicles = service.get_all_vehicles()
    return jsonify([v.serialize() for v in vehicles]), 200

@app.route("/vehicles/<int:vehicle_id>", methods=["GET"])
def get_vehicle(vehicle_id):
    vehicle = service.get_vehicle(vehicle_id)
    if vehicle:
        return jsonify(vehicle.serialize()), 200
    return jsonify({"error": "Vehicle not found"}), 404

@app.route("/users", methods=["GET"])
def get_all_users():
    users = service.get_all_users()
    return jsonify([u.serialize() for u in users]), 200

@app.route("/users/<int:user_id>/favorites", methods=["GET"])
def get_user_favorites(user_id):
    favorites = service.get_user_favorites(user_id)
    if favorites is not None:
        return jsonify(favorites), 200
    return jsonify({"error": "User not found"}), 404

@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(planet_id):
    user_id = request.json.get("user_id")
    favorite = service.add_favorite_planet(user_id, planet_id)
    return jsonify(favorite.serialize()), 201

@app.route("/favorite/people/<int:character_id>", methods=["POST"])
def add_favorite_character(character_id):
    user_id = request.json.get("user_id")
    favorite = service.add_favorite_character(user_id, character_id)
    return jsonify(favorite.serialize()), 201

@app.route("/favorite/vehicle/<int:vehicle_id>", methods=["POST"])
def add_favorite_vehicle(vehicle_id):
    user_id = request.json.get("user_id")
    favorite = service.add_favorite_vehicle(user_id, vehicle_id)
    return jsonify(favorite.serialize()), 201

@app.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(planet_id):
    user_id = request.json.get("user_id")
    if service.delete_favorite_planet(user_id, planet_id):
        return jsonify({"done": True}), 200
    return jsonify({"error": "Favorite not found"}), 404

@app.route("/favorite/people/<int:character_id>", methods=["DELETE"])
def delete_favorite_character(character_id):
    user_id = request.json.get("user_id")
    if service.delete_favorite_character(user_id, character_id):
        return jsonify({"done": True}), 200
    return jsonify({"error": "Favorite not found"}), 404

@app.route("/favorite/vehicle/<int:vehicle_id>", methods=["DELETE"])
def delete_favorite_vehicle(vehicle_id):
    user_id = request.json.get("user_id")
    if service.delete_favorite_vehicle(user_id, vehicle_id):
        return jsonify({"done": True}), 200
    return jsonify({"error": "Favorite not found"}), 404



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
