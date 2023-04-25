import json
import threading
import time

import pika
from configs import broker
from datetime import datetime
from configs.environment import rabbitHost, rabbitPassword, rabbitUsername
from tools import serverStatus, servers, alerts


lastVerificationTimes = {}

_credentials = pika.PlainCredentials(rabbitUsername(), rabbitPassword())
_parameters = pika.ConnectionParameters(rabbitHost(), 5672, "/", _credentials)


def init():
    broker.purgeQueue("keepAlive")

    lastVerificationTimes.update(
        {
            serverName: datetime.now()
            for serverName in servers.getNames()
            if serverName not in lastVerificationTimes
        }
    )

    threading.Thread(target=queueReciver).start()
    threading.Thread(target=onlineTimeValidation).start()


def queueReciver():
    connection = pika.BlockingConnection(_parameters)
    channel = connection.channel()

    channel.queue_declare(queue="keepAlive", durable=True)

    def __callback(ch, method, properties, body):
        body = json.loads(body.decode())
        serverName = body["serverName"]
        status = serverStatus.get(serverName)

        if status != body["status"]:
            alerts.send(f'{serverName} ({body["status"]})')

        serverStatus.set(serverName, body["status"])
        lastVerificationTimes[serverName] = datetime.now()

    channel.basic_consume(
        queue="keepAlive", on_message_callback=__callback, auto_ack=True
    )

    channel.start_consuming()

    channel.close()
    connection.close()


def onlineTimeValidation():
    while True:
        for serverName in lastVerificationTimes:
            if (
                datetime.now() - lastVerificationTimes[serverName]
            ).total_seconds() >= 5:
                if serverStatus.get(serverName) != "offline":
                    alerts.send(f"{serverName} (offline)")

                serverStatus.set(serverName, "offline")

        time.sleep(1)
