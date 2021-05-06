from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

from MQTTClient import MQTTClient


def ajob(mes):
    print(mes)
    from time import sleep
    sleep(8)


if __name__ == '__main__':
    sensor1, sensor2 = MQTTClient("sensor1sub"), MQTTClient("sensor2sub")
    #sensor1.connect("raspberry", "Pieroangela0", "37c7a072139e48e380bb5e3df6662706.s1.eu.hivemq.cloud", False)
    sensor2.connect("raspberry2", "Raspberry2", "37c7a072139e48e380bb5e3df6662706.s1.eu.hivemq.cloud", True)
    #sensor1.subscribe("comunication/Azienda1/frigo")
    sensor2.subscribe("comunication/Azienda1/frigo1")
