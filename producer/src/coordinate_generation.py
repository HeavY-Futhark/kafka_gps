import random
def generate_gps_coordinates():
    latitude = random.uniform(-90,90)
    longitude = random.uniform(-180,180)
    return {'latitude':latitude, 'longitude':longitude}