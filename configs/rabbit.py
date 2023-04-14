import json
import pika


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()


def sendMessage(queueName, queueMessage):
    channel.queue_declare(queue=queueName, durable=True)

    channel.basic_publish(
        exchange="",
        routing_key=queueName,
        body=json.dumps(queueMessage),
        properties=pika.BasicProperties(delivery_mode=2),
    )
