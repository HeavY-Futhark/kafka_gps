from confluent_kafka import Producer
import json
from producer.src.coordinate_tracker import generate_gps_coordinates, CoordinateTracker

# Fonction de callback pour rapport de livraison des messages
def delivery_report(err,msg):
    # Si une erreur est présente on affiche un message d'échec
    if (err != None):
        print('Message delivery failed: {}'.format(err))
    else:
        # Sinon, affiche un message indiquant que le message a été livré avec succès,
        # avec le nom du sujet (topic) et le numéro de partition associé
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

# Fonction pour créer et envoyer des messages GPS à Kafka
def create_gps_messages(bootstrap_servers='localhost:9092', topic='coordinates', num_messages=1 ):
    # Configuration du client Kafka, avec le serveur d'amorçage par défaut 'localhost:9092'
    config = {
        'bootstrap.servers' : bootstrap_servers
    }

    # Création d'une instance de producteur Kafka avec la configuration spécifiée
    producer = Producer(config)
    # Liste pour stocker les coordonnées GPS générées
    generated_coordinates = []

    try:

        # Création d'une instance de CoordinateTracker avec des valeurs initiales
        initial_coordinates = generate_gps_coordinates()
        initial_speed = 10.0
        initial_direction = 15.0
        tracker = CoordinateTracker(initial_coordinates['latitude'], initial_coordinates['longitude'],
                                     initial_speed, initial_direction)

        # Boucle pour générer et envoyer le nombre spécifié de messages GPS
        for _ in range(num_messages):
            #Génération de coordonnées GPS
            gps_coordinates = generate_gps_coordinates()
            #Ajout des coordonnées GPS
            generated_coordinates.append(gps_coordinates)
            #Conversion des coordonnées en json
            message_value = json.dumps(gps_coordinates)
            #Envoi du message au topic kafka specifié via la fonction de callback
            producer.produce(topic,value=message_value,callback=delivery_report)
            #Forçage de l'envoi immédiat du message (utile dans ce contexte)
            #producer.flush()
            time_elapsed = 1.0
            tracker.update_position(time_elapsed)

    except KeyboardInterrupt:
        pass
    finally:
        # Forçage de l'envoi de tout message restant et fermeture du producteur
        producer.flush()
        #producer.close()
    return generated_coordinates


if __name__ == "__main__":
    # Appel de la fonction create_gps_messages lors de l'exécution du script
    generated_coordinates = create_gps_messages()
    # Affichage des coordonnées GPS générées
    print("Generated Coordinates:", generated_coordinates)