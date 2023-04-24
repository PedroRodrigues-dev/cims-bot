import json
import threading
import time
from configs import broker
from datetime import datetime
from tools import serverStatus, servers, alerts, channels


lastVerificationTimes = {}


def init():
    broker.purgeQueue("keepAlive")

    t1 = threading.Thread(target=queueReciver)
    t2 = threading.Thread(target=onlineTimeValidation)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


def queueReciver():
    while True:
        message = broker.reciveMessage("keepAlive")

        if message:
            status = serverStatus.get(message["serverName"])

            if status == None or status.decode() != message["status"]:
                serverStatus.set(message["serverName"], message["status"])

                if channels.getAlert():
                    alerts.send(f'{message["serverName"]} ({message["status"]})')

            lastVerificationTimes[message["serverName"]] = datetime.now()

        time.sleep(1)


def onlineTimeValidation():
    while True:
        for server_name in lastVerificationTimes:
            if (
                datetime.now() - lastVerificationTimes[server_name]
            ).total_seconds() >= 5:
                if serverStatus.get(server_name).decode() != "offline":
                    serverStatus.set(server_name, "offline")
                    if channels.getAlert():
                        alerts.send(f"{server_name} (offline)")

        lastVerificationTimes.update(
            {
                server_name: datetime.now()
                for server_name in servers.getNames()
                if server_name not in lastVerificationTimes
            }
        )

        time.sleep(1)
