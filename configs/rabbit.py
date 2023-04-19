import json
import time
import pika

from configs.environment import (
    systemTimeout,
    rabbitHost,
    rabbitPassword,
    rabbitUsername,
)


def connect():
    credentials = pika.PlainCredentials(rabbitUsername(), rabbitPassword())
    parameters = pika.ConnectionParameters(rabbitHost(), 5672, "/", credentials)
    connection = None

    try:
        connection = pika.BlockingConnection(parameters)
    except pika.exceptions.AMQPConnectionError:
        connection = None

    while connection is None:
        print("Trying to reconnect with rabbitMQ")
        time.sleep(systemTimeout())
        connect()

    return connection


def sendMessage(queueName, queueMessage):
    connection = connect()

    queueName = f"{queueName}-bot"

    channel = connection.channel()

    channel.queue_declare(queue=queueName, durable=True)

    channel.basic_publish(
        exchange="",
        routing_key=queueName,
        body=json.dumps(queueMessage),
        properties=pika.BasicProperties(delivery_mode=2),
    )

    channel.close()

    connection.close()


def reciveMessages(queueName):
    if queueName:
        connection = connect()

        queueName = f"{queueName}-server"

        channel = connection.channel()

        channel.queue_declare(queue=queueName, durable=True)

        message = None

        def callback(ch, method, properties, body):
            nonlocal message
            message = body

        channel.basic_consume(queueName, on_message_callback=callback, auto_ack=True)

        timeout = int(systemTimeout())

        start_time = time.time()

        while message is None and (time.time() - start_time) < timeout:
            connection.process_data_events()

        connection.close()

        if message is not None:
            return json.loads(message.decode())
        else:
            return {"body": "no response from server"}
