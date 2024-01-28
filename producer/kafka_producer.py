import json
import logging
import time
from confluent_kafka import Producer
from coordinate_tracker import generate_gps_coordinates, CoordinateTracker
import os

ip = os.environ.get("IP_PRODUCER")

# Fonction de rappel pour les rapports de livraison
def delivery_report(err, msg):
    if err is not None:
        logging.error(f'Échec de la livraison du message : {err}')
    else:
        logging.info(f'Message livré à {msg.topic()} [{msg.partition()}]')

# Fonction pour créer et envoyer des messages GPS à Kafka
# num_messages = 0 pour infini
def create_gps_messages(bootstrap_servers='kafka:9092', topic='coordinates', num_messages=0):
    # Configuration du producteur Kafka
    config = {
        'bootstrap.servers': bootstrap_servers
    }
    producer = Producer(config)
    generated_coordinates = []

    # Génération de coordonnées GPS initiales
    initial_coordinates = {'latitude': 43.30, 'longitude': -0.37}
    initial_speed = 0.05
    initial_direction = 15.0
    # Initialisation du suivi des coordonnées
    tracker = CoordinateTracker(ip, initial_coordinates['latitude'], initial_coordinates['longitude'],
                                 initial_speed, initial_direction)

    try:
        iterator = iter(int, 1) if num_messages == 0 else range(num_messages)
        for _ in iterator:
            # Mise à jour de la position toutes les secondes
            tracker.update_position(1.0)
            # Récupération des coordonnées GPS
            gps_coordinates = tracker.get_coordinates()
            generated_coordinates.append(gps_coordinates)
            # Conversion des coordonnées en JSON et envoi au topic Kafka
            producer.produce(topic, value=gps_coordinates.to_json(), callback=delivery_report)

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
