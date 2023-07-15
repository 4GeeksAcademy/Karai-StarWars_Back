"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import (
    db,
    User,
    Character,
    Planet,
    Starship,
    Favorite_character,
    Favorite_planet,
    Favorite_starship,
)

# from models import Person

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.url_map.strict_slashes = False


db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url.replace(
        "postgres://", "postgresql://"
    )
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# generate sitemap with all your endpoints
@app.route("/")
def sitemap():
    return generate_sitemap(app)


@app.route("/users", methods=["POST"])
def create_user():
    try:

        username = request.json.get('username')
        mail = request.json.get('mail')
        password = request.json.get('password')

        if  not mail or not password:
            return jsonify({'error': 'Mail and password are required.'}), 400
        
        # existing_username=User.query.filter_by(username=username).first()
        # if existing_username:
        #     return jsonify({'error': 'Username already exist.'}), 409
        
        existing_mail=User.query.filter_by(mail=mail).first()
        if existing_mail:
            return jsonify({'error': 'Mail already exist.'}), 409
        
        db_passowrd = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username = username, mail = mail, password= db_passowrd)
        db.session.add(new_user)
        db.session.commit()

        response_body = {
            "username": new_user.username,
            "mail": new_user.mail,
        }

        return jsonify({"User created successfully": response_body}), 200
    
    except Exception as e:
        return jsonify({'error': 'Error in user creation: ' + str(e)}), 500

@app.route('/token', methods=['POST'])
def get_token():

    try:

        username = request.json.get('username')
        mail = request.json.get('mail')
        password = request.json.get('password')

        if not mail or not password:
            return({'error': 'Mail and password are required.'})
        
        
        

        
    except Exception as e:
        return jsonify({'error': 'Error of autentification: ' + str(e)}), 500


@app.route("/users", methods=["GET"])
def get_all_users():
    users = User.query.all()

    users_list = []
    for user in users:
        user_dict = {
            "id": user.id,
            "username": user.username,
            "mail": user.mail,
        }
        users_list.append(user_dict)

    return jsonify("List of users:", users_list), 200


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user = User.query.get(user_id)

    user_list = {
        "id": user.id,
        "username": user.username,
        "mail": user.mail,
    }

    if user:
        return jsonify(user_list)
    else:
        return jsonify({"error": "Not founded user"}), 404


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):

    new_username = request.json.get("username")
    user = User.query.get(user_id)
    user.username = new_username
    db.session.commit()

    new_data = {"username": user.username, "mail": user.mail, "password": user.password}

    return jsonify("Updated user", new_data)

@app.route("/character", methods=["POST"])
def post_character():

    characters = Character.query.all()

    character_list = []
    for char in characters:
        character_dict = {
            "id": char.id,
            "name": char.name,
            "birth_year": char.birth_year,
            "eye_color": char.eye_color,
            "hair_color": char.hair_color,
            "skin_color": char.skin_color,
            "gender": char.gender,
            "height": char.height,
            "mass": char.mass,
            "homeworld": char.homeworld,
        }
        character_list.append(character_dict)

        return jsonify(character_list)

@app.route("/character", methods=["GET"])
def get_all_character():

    characters = Character.query.all()

    character_list = []
    for char in characters:
        character_dict = {
            "id": char.id,
            "name": char.name,
            "birth_year": char.birth_year,
            "eye_color": char.eye_color,
            "hair_color": char.hair_color,
            "skin_color": char.skin_color,
            "gender": char.gender,
            "height": char.height,
            "mass": char.mass,
            "homeworld": char.homeworld,
        }
        character_list.append(character_dict)

        return jsonify(character_list)


@app.route("/character/<int:character_id>", methods=["GET"])
def get_character_by_id(character_id):
    character = Character.query.get(character_id)

    if not character:
        return jsonify({"error": "No character finded"}), 404
    
    character_list = {
            "id": character.id,
            "name": character.name,
            "birth_year": character.birth_year,
            "eye_color": character.eye_color,
            "hair_color": character.hair_color,
            "skin_color": character.skin_color,
            "gender": character.gender,
            "height": character.height,
            "mass": character.mass,
            "homeworld": character.homeworld,
        }

    return jsonify('Your character is:', character_list)


@app.route("/planets", methods=["GET"])
def get_all_planets():

    planets = Planet.query.all()

    planet_list = []
    for planet in planets:
        planet_dict = {
            'id': planet.id,
            'name': planet.name,
            'climate': planet.climate,
            'diameter': planet.diameter,
            'gravity': planet.gravity,
            'orbital_period': planet.orbital_period,
            'population': planet.population,
            'rotation_period': planet.rotation_period,
            'surface_water': planet.surface_water,
            'terrain': planet.terrain
        }
        planet_list.append(planet_dict)

    return jsonify(planet_list)


@app.route("/planets/<int:planet_id>", methods=["GET"])
def get_planet_by_id(planet_id):

    planet = Planet.query.get(planet_id)

    if not planet:
        return jsonify({"error": "No planet finded"}), 404

    planet_list = {
            'id': planet.id,
            'name': planet.name,
            'climate': planet.climate,
            'diameter': planet.diameter,
            'gravity': planet.gravity,
            'orbital_period': planet.orbital_period,
            'population': planet.population,
            'rotation_period': planet.rotation_period,
            'surface_water': planet.surface_water,
            'terrain': planet.terrain
        }

    return jsonify(planet_list)


@app.route("/ships", methods=["GET"])
def get_all_ships():
    ships = Starship.query.all()

    ship_list = []
    for ship in ships:
        ship_dict = {
            'id': ship.id,
            'name': ship.name,
            'model': ship.model,
            'MGLT': ship.MGLT,
            'cargo_capacity': ship.cargo_capacity,
            'consumable': ship.consumable,
            'cost_in_credits': ship.cost_in_credits,
            'crew': ship.crew,
            'hyperdrive_rating': ship.hyperdrive_rating,
            'length': ship.length,
            'manufacturer': ship.manufacturer,
            'max_atmospherix_speed': ship.max_atmospherix_speed
        }
        ship_list.append(ship_dict)

    return jsonify(ship_list)


@app.route("/ships/<int:ship_id>", methods=["GET"])
def get_ship_by_id(ship_id):
    ship = Starship.query.get(ship_id)

    if not ship:
        return jsonify({"error": "No StarShip finded"}), 404
    
    ship_list = {
            'id': ship.id,
            'name': ship.name,
            'model': ship.model,
            'MGLT': ship.MGLT,
            'cargo_capacity': ship.cargo_capacity,
            'consumable': ship.consumable,
            'cost_in_credits': ship.cost_in_credits,
            'crew': ship.crew,
            'hyperdrive_rating': ship.hyperdrive_rating,
            'length': ship.length,
            'manufacturer': ship.manufacturer,
            'max_atmospherix_speed': ship.max_atmospherix_speed
        }

    return jsonify(ship_list)


@app.route("/favorites/<int:user_id>", methods=["GET"])
def get_user_favorites(user_id):

    favorite_characters = db.session.query(Favorite_character).filter_by(user_id=user_id).all()    
    favorite_character_ids = [fav.character_id for fav in favorite_characters]    
    favorite_planets = db.session.query(Favorite_planet).filter_by(user_id=user_id).all()    
    favorite_planets_ids = [fav.planet_id for fav in favorite_planets]   
    favorite_ships = db.session.query(Favorite_starship).filter_by(user_id=user_id).all()    
    favorite_ships_ids = [fav.starship_id for fav in favorite_ships]   

    favorites = {
        "character": favorite_character_ids,
        "planets": favorite_planets_ids,
        "ships": favorite_ships_ids,
    }

    return jsonify(favorites)


# @app.route('/favorites/character', methods=['POST'])
# def post_favorite_character():

#     data = request.json
#     favorite = Favorite_character(character_id = data['character_id'], user_id = data['user_id'])
#     db.session.add(favorite)
#     db.session.commit()

#     return jsonify('Favorite character added')

@app.route('/favorites/planet', methods=['POST'])
def post_favorite_planet():

    data = request.json
    favorite = Favorite_planet(planet_id = data['planet_id'], user_id = data['user_id'])
    db.session.add(favorite)
    db.session.commit()

    return jsonify('Favorite planet added')

# @app.route('/favorites/ships', methods=['POST'])
# def post_favorite_ship():

#     data = request.json

#     favorite = Starship(starship_id=data['starship_id'], user_id=data['user_id'])
#     db.session.add(favorite)
#     db.session.commit()
#     # properties_ids = {
#     #     "character_id": favorite.character_id,
#     #     "user_id": favorite.user_id
#     # }

#     return ('Favorite character added')

@app.route('/favorites/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character():

    return

@app.route('/favorites/planet/<int:favorite_id>', methods=['DELETE'])
def delete_favorite_planet():

    return

@app.route('/favorites/ships/<int:ship_id>', methods=['DELETE'])
def delete_favorite_ship():

    return

# this only runs if `$ python src/app.py` is executed
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=False)
