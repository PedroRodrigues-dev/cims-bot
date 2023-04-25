import json
import time
import threading
import pika

from configs.environment import (
    rabbitHost,
    rabbitPassword,
    rabbitUsername,
)

_credentials = pika.PlainCredentials(rabbitUsername(), rabbitPassword())
_parameters = pika.ConnectionParameters(rabbitHost(), 5672, "/", _credentials)


def getConnection():
    return pika.BlockingConnection(_parameters)


def sendMessage(queueName, message):
    if queueName and message:
        connection = getConnection()

        channel = connection.channel()

        channel.queue_declare(queue=queueName, durable=True)

        channel.basic_publish(
            exchange="",
            routing_key=queueName,
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2),
        )

        channel.close()
        connection.close()

        return True
    else:
        return False


def purgeQueue(queueName):
    connection = getConnection()
    channel = connection.channel()

    channel.queue_declare(queue=queueName, durable=True)
    channel.queue_purge(queueName)

    channel.close()
    connection.close()
