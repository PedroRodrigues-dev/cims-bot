from datetime import datetime
import json
import time
import pika

from configs.environment import (
    systemTimeout,
    rabbitHost,
    rabbitPassword,
    rabbitUsername,
)

_credentials = pika.PlainCredentials(rabbitUsername(), rabbitPassword())
_parameters = pika.ConnectionParameters(rabbitHost(), 5672, "/", _credentials)
_connection = None


def getConnection():
    global _connection

    while not _connection or _connection.is_closed:
        try:
            _connection = pika.BlockingConnection(_parameters)
        except pika.exceptions.AMQPConnectionError:
            _connection = None
            print("Trying to reconnect with rabbitMQ")
            time.sleep(systemTimeout())

    return _connection


def sendMessage(queueName, queueMessage):
    if queueName and queueMessage:
        connection = getConnection()

        channel = connection.channel()

        channel.queue_declare(queue=queueName, durable=True)

        channel.basic_publish(
            exchange="",
            routing_key=queueName,
            body=json.dumps(queueMessage),
            properties=pika.BasicProperties(delivery_mode=2),
        )

        channel.close()

        return True
    else:
        return False


def reciveMessage(queueName):
    connection = getConnection()
    channel = connection.channel()
    channel.queue_declare(queue=queueName, durable=True)

    messageReceived = None
    attempts = systemTimeout()
    while not messageReceived and attempts > 0:
        method_frame, header_frame, body = channel.basic_get(
            queue=queueName, auto_ack=True
        )
        if body is not None:
            messageReceived = json.loads(body.decode())
        else:
            time.sleep(1)
            attempts -= 1

    channel.close()

    if messageReceived:
        return messageReceived
    else:
        return False


def purgeQueue(queueName):
    connection = getConnection()
    channel = connection.channel()

    channel.queue_declare(queue=queueName, durable=True)
    channel.queue_purge(queueName)

    channel.close()
