from models import db, Character, Planet, Vehicle, FavoriteCharacter, FavoritePlanet, FavoriteVehicle, User

class StarWarsService:
    
    def get_all_characters(self):
        return Character.query.all()

    def get_character(self, character_id):
        return Character.query.get(character_id)

    
    def get_all_planets(self):
        return Planet.query.all()

    def get_planet(self, planet_id):
        return Planet.query.get(planet_id)

    
    def get_all_vehicles(self):
        return Vehicle.query.all()

    def get_vehicle(self, vehicle_id):
        return Vehicle.query.get(vehicle_id)

    
    def get_all_users(self):
        return User.query.all()

    
    def get_user_favorites(self, user_id):
        user = User.query.get(user_id)
        if user:
            return {
                "favorite_characters": [c.serialize() for c in user.favorite_characters],
                "favorite_planets": [p.serialize() for p in user.favorite_planets],
                "favorite_vehicles": [v.serialize() for v in user.favorite_vehicles],
            }
        return None

    def add_favorite_character(self, user_id, character_id):
        favorite = FavoriteCharacter(user_id=user_id, character_id=character_id)
        db.session.add(favorite)
        db.session.commit()
        return favorite

    def delete_favorite_character(self, user_id, character_id):
        favorite = FavoriteCharacter.query.filter_by(user_id=user_id, character_id=character_id).first()
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            return True
        return False

    def add_favorite_planet(self, user_id, planet_id):
        favorite = FavoritePlanet(user_id=user_id, planet_id=planet_id)
        db.session.add(favorite)
        db.session.commit()
        return favorite

    def delete_favorite_planet(self, user_id, planet_id):
        favorite = FavoritePlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            return True
        return False

    def add_favorite_vehicle(self, user_id, vehicle_id):
        favorite = FavoriteVehicle(user_id=user_id, vehicle_id=vehicle_id)
        db.session.add(favorite)
        db.session.commit()
        return favorite

    def delete_favorite_vehicle(self, user_id, vehicle_id):
        favorite = FavoriteVehicle.query.filter_by(user_id=user_id, vehicle_id=vehicle_id).first()
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            return True
        return False
