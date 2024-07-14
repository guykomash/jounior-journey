from confluent_kafka import Consumer
import listeners
import sys
import signal
from dotenv import load_dotenv
import os

load_dotenv()
KAFKA_SERVER = os.getenv('KAFKA_SERVER')
KAFKA_USERNAME = os.getenv('KAFKA_USERNAME')
KAFKA_PASSWORD = os.getenv('KAFKA_PASSWORD')

consumer = Consumer({
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


def kafka_consumer():
    print("consuming kakfa...")
    consumer.subscribe(['pdf_compress_complete_topic'])
    try:
        while True:
            # consumer polls the topic and prints any incoming messages
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f'Consumer error: {msg.error()}')
                continue
            
            print(msg.key().decode("utf-8"))
            # activate callback function
            try:
                getattr(listeners, msg.key().decode('utf-8'))((msg.value()))
            except AttributeError as err:
                print(err)
    except KeyboardInterrupt:
        pass
    finally:
        # closes the consumer connection
        consumer.close()


def signal_handler(signal, frame):
    print('Shutting down gracefully...')
    consumer.close()  # Close the Kafka consumer
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)  # Handle Ctrl+C
signal.signal(signal.SIGTERM, signal_handler)  # Handle termination signals



if __name__ == "__main__":
    kafka_consumer()
