from confluent_kafka import Consumer, KafkaError
import json
import logging

# Fonction pour consommer des coordonnées GPS depuis Kafka
def consume_gps_coordinates(bootstrap_servers='localhost:9092', group_id='gps_consumer_group', topic='coordinates'):
    # Configuration du consommateur Kafka
    config = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'  # Commence à lire depuis le début du topic
    }

    # Création d'une instance de consommateur Kafka avec la configuration spécifiée
    consumer = Consumer(config)
    # Abonnement au topic spécifié
    consumer.subscribe([topic])
    logging.info("Consommateur Kafka démarré. En attente de messages...")

    try:
        while True:
            # Lecture des messages du topic
            msg = consumer.poll(timeout=1.0)

            # Continuer si aucun message n'est récupéré
            if msg is None:
                continue
            # Gestion des erreurs éventuelles
            if msg.error():
                # Gestion de la fin de la partition
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logging.info('Fin de la partition atteinte {0}/{1}'
                                 .format(msg.topic(), msg.partition()))
                else:
                    # En cas d'autre erreur, affichage de l'erreur et arrêt du consommateur
                    logging.error(msg.error())
                    break

            try:
                # Décodage et traitement des coordonnées GPS
                gps_coordinates = json.loads(msg.value().decode('utf-8'))
                process_gps_coordinates(gps_coordinates)
            except json.JSONDecodeError as e:
                # Gestion des erreurs de décodage JSON
                logging.error(f"Erreur de décodage JSON : {e}")

    except KeyboardInterrupt:
        # Gestion de l'interruption par l'utilisateur (Ctrl+C)
        logging.info("Signal d'arrêt reçu. Fermeture du consommateur...")
        consumer.close()
        logging.info("Consommateur fermé. Sortie...")
    finally:
        # Fermeture du consommateur dans tous les cas
        consumer.close()

def process_gps_coordinates(coordinates):
    # Traitement des coordonnées GPS reçues
    logging.info(f"Traitement des coordonnées GPS : {coordinates}")

if __name__ == "__main__":
    # Configuration du journal (logging)
    logging.basicConfig(level=logging.INFO)
    consume_gps_coordinates()
