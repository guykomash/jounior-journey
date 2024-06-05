from confluent_kafka import Producer
from dotenv import load_dotenv
import os

load_dotenv()

KAFKA_SERVER = os.getenv('KAFKA_SERVER')
KAFKA_USERNAME = os.getenv('KAFKA_USERNAME')
KAFKA_PASSWORD = os.getenv('KAFKA_PASSWORD')

producer = Producer({
    'bootstrap.servers': KAFKA_SERVER,
    'security.protocol':'SASL_SSL',
    'sasl.mechanisms':'PLAIN',
    'sasl.username': KAFKA_USERNAME,
    'sasl.password':KAFKA_PASSWORD,
    'group.id':'pythob-group-1',
    'auto.offset.reset':'earliest',

    # Best practice for higher availability in librdkafka clients prior to 1.7
    'session.timeout.ms':'45000',
})



def produce_msg(topic, key, value):
    producer.produce(topic=topic, key=key, value=value)
    print(f"Produced message to {topic}")
    producer.flush()