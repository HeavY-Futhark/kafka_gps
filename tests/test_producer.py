import json
from unittest.mock import MagicMock, patch
import pytest

import sys
sys.path.append('/producer/src')

from producer.src.kafka_producer import create_gps_messages

#from ..producer.src.kafka_producer import create_gps_messages

#simulation (mock) de la classe Producer
@pytest.fixture
def mock_producer():
    with patch('producer.src.kafka_producer.Producer') as mock_producer_class:
        # Création d'une instance de mock pour la classe Producer
        mock_producer_instance = MagicMock()
        mock_producer_class.return_value = mock_producer_instance
        # Rend l'instance du mock disponible pour le test
        yield mock_producer_instance
#simulation (mock) pour la fonction generate_gps_coordinates
@pytest.fixture
def mock_generate_gps_coordinates():
    with patch('producer.src.kafka_producer.generate_gps_coordinates') as mock_generate_coordinates:
        # Création d'une instance de mock pour la fonction generate_gps_coordinates
        mock_generate_coordinates.return_value = {'latitude': 1.23, 'longitude': 4.56}
        # Rend l'instance du mock disponible pour le test
        yield mock_generate_coordinates

def test_create_gps_messages(mock_producer, mock_generate_gps_coordinates):
    # Appel de la fonction à tester
    generated_coordinates = create_gps_messages()

    assert len(generated_coordinates) == 1  # Adjust based on the actual number of messages generated
    assert isinstance(generated_coordinates[0], dict)
    assert 'latitude' in generated_coordinates[0]
    assert 'longitude' in generated_coordinates[0]

    mock_producer.produce.assert_called()
    mock_producer.flush.assert_called()
    mock_generate_gps_coordinates.assert_called()
    
if __name__ == '__main__':
    pytest.main()