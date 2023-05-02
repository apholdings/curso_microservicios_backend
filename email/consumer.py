import json, os, django
from confluent_kafka import Consumer


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()
from rest_framework.exceptions import ValidationError

consumer = Consumer({
    'bootstrap.servers': os.environ.get('KAFKA_BOOTSTRAP_SERVER'),
    'security.protocol': os.environ.get('KAFKA_SECURITY_PROTOCOL'),
    'sasl.username': os.environ.get('KAFKA_USERNAME'), 
    'sasl.password': os.environ.get('KAFKA_PASSWORD'),
    'sasl.mechanism': 'PLAIN',
    'group.id': os.environ.get('KAFKA_GROUP'),
    'auto.offset.reset': 'earliest'
})

consumer.subscribe([os.environ.get('KAFKA_TOPIC')])

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue

    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    if msg is not None and not msg.error():

        topic = msg.topic()
        value = msg.value()

        data = json.loads(value)
        # print(f'Got this message with Topic: {topic} and value: {value}, with Data: {data}')
        
        # if topic == os.environ.get('KAFKA_TOPIC'):
        #     if msg.key() == b'create_user':
        #         try:
        #             print(f"Order created successfully for user {data['userID']}")
        #         except ValidationError as e:
        #             print(f"Failed to create order for user {data['userID']}: {str(e)}")

consumer.close()