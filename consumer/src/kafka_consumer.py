from confluent_kafka import Consumer, KafkaError
import json

def consume_gps_coordinates(bootstrap_servers='localhost:9092', group_id='gps_consumer_group', topic='coordinates'):
    config = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'  # Début du traitement au debut du topic
    }

    consumer = Consumer(config)
    consumer.subscribe([topic])

    try:
        while True:
            msg = consumer.poll(timeout=1000)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            # Decode et process les coordonnées GPS
            try:
                gps_coordinates = json.loads(msg.value().decode('utf-8'))
                process_gps_coordinates(gps_coordinates)  # Fonction de traitement des coordonnées
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

def process_gps_coordinates(coordinates):
    # Traitement des coordonnées GPS
    print("Processing GPS Coordinates:", coordinates)

if __name__ == "__main__":
    consume_gps_coordinates()
