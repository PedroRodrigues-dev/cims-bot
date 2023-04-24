import threading
import time
from configs import broker
from datetime import datetime
from tools import serverStatus, servers, alerts


lastVerificationTimes = {}


def init():
    broker.purgeQueue("keepAlive")

    threading.Thread(target=queueReciver).start()
    threading.Thread(target=onlineTimeValidation).start()


def queueReciver():
    while True:
        message = broker.reciveMessage("keepAlive")

        if message:
            serverName = message["serverName"]
            status = serverStatus.get(serverName)

            if status != message["status"]:
                alerts.send(f'{serverName} ({message["status"]})')

            serverStatus.set(serverName, message["status"])
            lastVerificationTimes[serverName] = datetime.now()

        time.sleep(1)


def onlineTimeValidation():
    while True:
        for serverName in lastVerificationTimes:
            if (
                datetime.now() - lastVerificationTimes[serverName]
            ).total_seconds() >= 5:
                if serverStatus.get(serverName) != "offline":
                    alerts.send(f"{serverName} (offline)")

                serverStatus.set(serverName, "offline")

        lastVerificationTimes.update(
            {
                server_name: datetime.now()
                for server_name in servers.getNames()
                if server_name not in lastVerificationTimes
            }
        )
        time.sleep(1)
