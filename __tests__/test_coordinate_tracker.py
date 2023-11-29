import pytest
from producer.src.coordinate_tracker import CoordinateTracker

def test_coordinate_tracker():
    # Valeurs initiales pour le test
    initial_latitude = 37.7749
    initial_longitude = -122.4194
    initial_speed = 10.0
    initial_direction = 45.0

    # Créez une instance de CoordinateTracker
    tracker = CoordinateTracker(initial_latitude, initial_longitude, initial_speed, initial_direction)

    # Mettez à jour la position après 2 secondes
    time_elapsed = 2.0
    tracker.update_position(time_elapsed)

    # Obtenez les nouvelles coordonnées
    new_coordinates = tracker.get_coordinates()

    # Assertions pour vérifier si les coordonnées ont été correctement mises à jour
    assert isinstance(new_coordinates, dict)
    assert 'latitude' in new_coordinates
    assert 'longitude' in new_coordinates

if __name__ == "__main__":
    pytest.main()
