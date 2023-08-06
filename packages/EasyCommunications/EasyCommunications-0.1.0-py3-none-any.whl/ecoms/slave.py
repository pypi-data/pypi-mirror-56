from EasyCommunicationHandler import EasyCommunicationSlave
import logging
import time

logging.addLevelName(10, "Slave-Debug")

i = 0
slave = EasyCommunicationSlave("localhost", 12456, "test")
while True:
    data = slave.wait_until_receiving()
    print("received by slave", data)

    i += 1
    time.sleep(i)
    slave.send(payload="slave responding")
