import json
import logging
import time
from confluent_kafka import Producer
from coordinate_tracker import generate_gps_coordinates, CoordinateTracker

# Fonction de rappel pour les rapports de livraison
def delivery_report(err, msg):
    if err is not None:
        logging.error(f'Échec de la livraison du message : {err}')
    else:
        logging.info(f'Message livré à {msg.topic()} [{msg.partition()}]')

# Fonction pour créer et envoyer des messages GPS à Kafka
def create_gps_messages(bootstrap_servers='localhost:9092', topic='coordinates', num_messages=1):
    # Configuration du producteur Kafka
    config = {
        'bootstrap.servers': bootstrap_servers
    }
    producer = Producer(config)
    generated_coordinates = []

    # Génération de coordonnées GPS initiales
    initial_coordinates = generate_gps_coordinates()
    initial_speed = 10.0
    initial_direction = 15.0
    # Initialisation du suivi des coordonnées
    tracker = CoordinateTracker(initial_coordinates['latitude'], initial_coordinates['longitude'],
                                 initial_speed, initial_direction)

    try:
        for _ in range(num_messages):
            # Mise à jour de la position toutes les secondes
            tracker.update_position(1.0)
            # Récupération des coordonnées GPS
            gps_coordinates = tracker.get_coordinates()
            generated_coordinates.append(gps_coordinates)
            # Conversion des coordonnées en JSON et envoi au topic Kafka
            message_value = json.dumps(gps_coordinates)
            producer.produce(topic, value=message_value, callback=delivery_report)

            # Sondage du producteur pour les événements, y compris les rapports de livraison
            producer.poll(0)

            # Simulation du temps écoulé pour la génération de la prochaine coordonnée GPS
            time.sleep(1.0)

    except KeyboardInterrupt:
        # Interruption par l'utilisateur (Ctrl+C)
        logging.info("Producteur interrompu. Sortie en cours...")
    finally:
        # Attente de la livraison de tous les messages en attente et fermeture du producteur
        producer.flush()
        logging.info("Producteur fermé.")

    return generated_coordinates

if __name__ == "__main__":
    # Configuration du journal (logging)
    logging.basicConfig(level=logging.INFO)
    generated_coordinates = create_gps_messages()
    logging.info(f"Coordonnées générées : {generated_coordinates}")
