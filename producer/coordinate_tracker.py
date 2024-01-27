import math
from datetime import datetime
from models.coordinate_model import Coordinate
import random

class CoordinateTracker:
    def __init__(self, ip, initial_latitude, initial_longitude, initial_speed, initial_direction):
        # Initialisation des coordonnées et de la direction
        self.ip = ip
        self.latitude = initial_latitude
        self.longitude = initial_longitude
        self.speed = initial_speed
        self.direction = initial_direction

    def update_position(self, time_elapsed):
        # Conversion de la direction en radians
        direction_in_radians = math.radians(self.direction)
        # Calcul des changements de latitude et longitude en fonction du temps écoulé
        delta_latitude = self.speed * math.cos(direction_in_radians) * time_elapsed
        delta_longitude = self.speed * math.sin(direction_in_radians) * time_elapsed

        self.latitude += delta_latitude
        self.longitude += delta_longitude

    def get_coordinates(self):
        # Renvoie les coordonnées actuelles
        return Coordinate(
            self.ip,
            datetime.now(),
            self.latitude,
            self.longitude
        )


###########################

#Fonction de génération de coordonnées aléatoires
def generate_gps_coordinates():
    latitude = random.uniform(-90,90)
    longitude = random.uniform(-180,180)
    return {'latitude':latitude, 'longitude':longitude}
    
if __name__ == '__main__':

    # Exemple d'utilisation
    initial_coordinates = generate_gps_coordinates()
    initial_speed = 10.0
    initial_direction = 15.0

    tracker = CoordinateTracker(0, initial_coordinates['latitude'], initial_coordinates['longitude'], initial_speed, initial_direction)

    # Mis à jour de la position après une certaine période de temps
    time_elapsed = 1.0
    tracker.update_position(time_elapsed)

    # Obtenez les nouvelles coordonnées
    new_coordinates = tracker.get_coordinates()
    print("Nouvelles coordonnées:", new_coordinates)
