import json
import os
from typing import Dict

import pika

RABBIT_HOST = os.environ.get('BWI_RABBIT_HOSTNAME')
RABBIT_VHOST = os.environ.get('RABBIT_VHOST')
RABBIT_USERID = os.environ.get('BWI_RABBIT_USER')
RABBIT_PASSWORD = os.environ.get('BWI_RABBIT_PASSWORD')
RABBIT_CREDENTIALS = pika.PlainCredentials(RABBIT_USERID, RABBIT_PASSWORD)
_rabbit_channel = None


class RabbitMQConnection:
    class __RabbitMQConnection:
        rabbit_channel = None
        rabbit_internals_channel = None

        def __init__(self):
            print(RABBIT_VHOST)
            rabbit_connection = pika.SelectConnection(
                pika.ConnectionParameters(host=RABBIT_HOST,
                                          credentials=RABBIT_CREDENTIALS,
                                          virtual_host=RABBIT_VHOST))
            self.rabbit_channel = rabbit_connection.channel()

            internals_rabbit_connection = pika.SelectConnection(
                pika.ConnectionParameters(host=RABBIT_HOST,
                                          credentials=RABBIT_CREDENTIALS,
                                          virtual_host="internals/"))
            self.rabbit_internals_channel = \
                internals_rabbit_connection.channel()

    instance = None

    def __init__(self):
        if not RabbitMQConnection.instance:
            RabbitMQConnection.instance = \
                RabbitMQConnection.__RabbitMQConnection()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def send_to_queue(self, queue_name: str, message: Dict):
        message = json.dumps(message)
        self.rabbit_channel.basic_publish(exchange='',
                                          routing_key=queue_name,
                                          body=message)
        print('Sent message "' + message + '" to queue "' + queue_name + '"')

    def send_to_internal_queue(self, queue_name: str, message: Dict):
        message = json.dumps(message)
        print(self.rabbit_internals_channel.basic_publish(exchange='',
                                                          routing_key=queue_name,
                                                          body=message))
        print('Sent message "' + message + '" to internal queue "' + queue_name + '"')
