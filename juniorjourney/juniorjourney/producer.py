from confluent_kafka import Producer


topic = "default"

producer = Producer({
    'bootstrap.servers':'pkc-7rgxp.il-central-1.aws.confluent.cloud:9092',
    'security.protocol':'SASL_SSL',
    'sasl.mechanisms':'PLAIN',
    'sasl.username':'F7JAPZ6WCHJLBZ44',
    'sasl.password':'C76nZ9QAIizl7pjLYwJ+mpmqe8ru0eLUT0CwDzBuuQEy28d7FT9M50N10Gzc6Jco',
    'group.id':'pythob-group-1',
    'auto.offset.reset':'earliest',

    # Best practice for higher availability in librdkafka clients prior to 1.7
    'session.timeout.ms':'45000',
})



def produce_msg(topic, key, value):
    producer.produce(topic=topic, key=key, value=value)
    print(f"Produced message to {topic}: key = {key:12} value = {value:12}")
    # send any outstanding or buffered messages to the Kafka broker
    producer.flush()