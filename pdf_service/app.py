from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from confluent_kafka import Consumer
# import requests
import threading
import listeners
import sys
import signal
import os
from flask_sqlalchemy import SQLAlchemy


KAFKA_SERVER = os.getenv('KAFKA_SERVER')
KAFKA_USERNAME = os.getenv('KAFKA_USERNAME')
KAFKA_PASSWORD = os.getenv('KAFKA_PASSWORD')

app = Flask(__name__)

# Kafka Consumer
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
    "consuming kakfa..."
    consumer.subscribe(['pdf_topic'])
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
            # invoke listener function by the message attribute.
            getattr(listeners, msg.key().decode('utf-8'))((msg.value()))
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

mysql_username = os.getenv('MYSQL_USERNAME')
mysql_password = os.getenv('MYSQL_PASSWORD')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{mysql_username}:{mysql_password}@localhost:3306/pdf_compressor'

db = SQLAlchemy(app)


@app.route('/')
def index():
    return "PDF Compression Service is running."

@app.route('/about')
def about():
    return "A service that compresses pdfs"


if __name__ == "__main__":
    consumer_thread = threading.Thread(target=kafka_consumer)
    consumer_thread.daemon = True  # Set as daemon
    consumer_thread.start()
    app.run(host='0.0.0.0', port=5000)