import pika
from configs.rabbit import connect

def send(message):
    connection = connect()

    queueName = "alerts"

    channel = connection.channel()

    channel.queue_declare(queue=queueName, durable=True)

    channel.basic_publish(
        exchange="",
        routing_key=queueName,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2),
    )

    channel.close()

    connection.close()