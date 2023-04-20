import json
import threading
from time import sleep
from configs import rabbit, redis
from datetime import datetime
from tools import serverStatus, servers, alerts


lastVerificationTimes = {}


def init():
    t1 = threading.Thread(target=queueReciver)
    t2 = threading.Thread(target=onlineTimeValidation)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


def queueReciver():
    connection = rabbit.connect()

    queueName = "keepAlive"

    channel = connection.channel()

    channel.queue_declare(queue=queueName, durable=True)

    def callback(ch, method, properties, body):
        body = json.loads(body)

        if serverStatus.get(body["serverName"]) == None or serverStatus.get(body["serverName"]).decode() != body["status"]:
            serverStatus.set(body["serverName"], body["status"])
            alerts.send(f'{body["serverName"]} ({body["status"]})')

        lastVerificationTimes[body["serverName"]] = datetime.now()

    channel.basic_consume(queueName, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


def onlineTimeValidation():
    while 1:
        for serverName in lastVerificationTimes:
            if (
                datetime.now() - lastVerificationTimes[serverName]
            ).total_seconds() >= 5:
                if serverStatus.get(serverName).decode() != "offline":
                    serverStatus.set(serverName, "offline")
                    alerts.send(f'{serverName} (offline)')


        for serverName in servers.getNames():
            if serverName not in lastVerificationTimes:
                lastVerificationTimes[serverName] = datetime.now()

        sleep(2)
