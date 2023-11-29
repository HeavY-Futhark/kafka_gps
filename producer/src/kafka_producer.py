from confluent_kafka import Producer
import json
from coordinate_generation import generate_gps_coordinates

def delivery_report(err,msg):
    if (err != None):
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

def create_gps_messages(bootstrap_servers='localhost:9092', topic='coordinates', num_messages=1 ):
    config = {
        'bootstrap.servers' : bootstrap_servers
    }

    producer = Producer(config)
    generated_coordinates = []

    try:
        for _ in range(num_messages):
            gps_coordinates = generate_gps_coordinates()
            generated_coordinates.append(gps_coordinates)
            message_value = json.dumps(gps_coordinates)

            producer.produce(topic,value=message_value,callback=delivery_report)
            producer.flush()
    except KeyboardInterrupt:
        pass
    finally:
        producer.flush()
        #producer.close()
    return generated_coordinates


if __name__ == "__main__":
    generated_coordinates = create_gps_messages()
    print("Generated Coordinates:", generated_coordinates)