import django
import json
import os
from confluent_kafka import Consumer


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

import core.listeners

consumer = Consumer({
'bootstrap.servers':'pkc-7rgxp.il-central-1.aws.confluent.cloud:9092',
'security.protocol':'SASL_SSL',
'sasl.mechanisms':'PLAIN',
'sasl.username':'F7JAPZ6WCHJLBZ44',
'sasl.password':'C76nZ9QAIizl7pjLYwJ+mpmqe8ru0eLUT0CwDzBuuQEy28d7FT9M50N10Gzc6Jco',
'group.id':'subscriptions-group',
'auto.offset.reset':'earliest',

# Best practice for higher availability in librdkafka clients prior to 1.7
'session.timeout.ms':'45000',
})



consumer.subscribe(['subscription_topic'])

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
        getattr(core.listeners, msg.key().decode('utf-8'))(json.loads(msg.value()))
except KeyboardInterrupt:
    pass
finally:
    # closes the consumer connection
    consumer.close()