import json, os, django
from confluent_kafka import Consumer
from contextlib import closing
import logging
logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.apps import apps

Author = apps.get_model('posts', 'Author')

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

def create_user(data):
    try:
        Author.objects.create(
            id=data['id'],
            username=data['username'],
            email=data['email']
        )
        logger.info(f"User created successfully")
    except Exception as e:
        logger.error(f"Failed to create user: {str(e)}")

    return

def edit_user(data):
    try:
        author = Author.objects.get(id=data['id'])
        author(
            id=data['id'],
            username=data['username'],
            email=data['email']
        )
        author.save()
        logger.info(f"User edited successfully")
    except Exception as e:
        logger.error(f"Failed to edit user: {str(e)}")

    return

with closing(consumer):
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            logger.error(f"Consumer error: {msg.error()}")
            continue

        if msg is not None and not msg.error():

            topic = msg.topic()
            value = msg.value()

            data = json.loads(value)
            
            if topic == os.environ.get('KAFKA_TOPIC'):
                if msg.key() == b'create_user':
                    try:
                        create_user(data)
                    except ValidationError as e:
                        logger.error(f"Failed to create user: {str(e)}")
                if msg.key() == b'edit_user':
                    try:
                        edit_user(data)
                    except ValidationError as e:
                        logger.error(f"Failed to edit user: {str(e)}")