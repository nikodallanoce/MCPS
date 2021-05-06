import threading
import time

import adafruit_dht
from adafruit_dht import DHT22
import board
from apscheduler.schedulers.blocking import BlockingScheduler

from MQTTClient import MQTTClient


def measure(device):
    read_correctly = False
    ris = ""
    while not read_correctly:
        try:
            t, h = device.temperature, device.humidity
            if t is None or h is None:
                read_correctly = False
            else:
                read_correctly = True
                print("temp: {0}'C - hum: {1}%".format(t, h))
                ris = "{0};{1}".format(t, h)
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print("Dev {0}".format(error.args[0]))
        except Exception as error:
            device.exit()
            raise error
    return ris


def old_main():
    # th = measure(devices[0])
    sensor1, sensor2 = MQTTClient("sensor1"), MQTTClient("sensor2")
    sensor1.connect("raspberry", "Pieroangela0", "37c7a072139e48e380bb5e3df6662706.s1.eu.hivemq.cloud", True)
    sensor2.connect("raspberry2", "Raspberry2", "37c7a072139e48e380bb5e3df6662706.s1.eu.hivemq.cloud", True)

    sensor1.publish("customer/Azienda1/frigo", measure(devices[0]))
    sensor2.publish("customer/Azienda1/frigo1", measure(devices[1]))
    sensor1.disconnect()
    sensor2.disconnect()

    sensor1, sensor2 = MQTTClient("sensor1sub"), MQTTClient("sensor2sub")
    sensor1.connect("raspberry", "Pieroangela0", "37c7a072139e48e380bb5e3df6662706.s1.eu.hivemq.cloud", False)
    sensor2.connect("raspberry2", "Raspberry2", "37c7a072139e48e380bb5e3df6662706.s1.eu.hivemq.cloud", False)
    sensor1.subscribe("comunication/Azienda1/frigo")
    sensor2.subscribe("comunication/Azienda1/frigo1")


def send_a_sample_to_topic(client: MQTTClient, sensor, usr: str, psw: str, con_str: str, pub_topic: str,
                           sub_topic: str, sub):
    client.connect(usr, psw, con_str, False)
    client.publish(pub_topic, measure(sensor))
    client.disconnect()
    modify_thr_sleep_time(sub, usr, psw, con_str, sub_topic)


def modify_thr_sleep_time(sub: MQTTClient, usr: str, psw: str, con_str: str, topic: str):
    sub.connect(usr, psw, con_str, False)
    sub.subscribe(topic)


def thread_start(args, iter):
    for i in range(iter):
        thr = threading.Thread(target=send_a_sample_to_topic,
                               args=args)
        thr.start()
        thr.join()


if __name__ == '__main__':
    devices = [DHT22(board.D4, False), DHT22(board.D18, False)]
    client1, client2 = MQTTClient("sensor1"), MQTTClient("sensor2")
    sub1, sub2 = MQTTClient("sensor1sub"), MQTTClient("sensor2sub")
    conn = "37c7a072139e48e380bb5e3df6662706.s1.eu.hivemq.cloud"
    start = time.time()

    th1 = threading.Thread(target=thread_start,
                           args=[[client1, devices[0], "raspberry", "Pieroangela0", conn, "customer/Azienda1/frigo",
                                  "comunication/Azienda1/frigo", sub1], 2])
    th2 = threading.Thread(target=thread_start,
                           args=[[client2, devices[1], "raspberry2", "Raspberry2", conn, "customer/Azienda1/frigo1",
                                  "comunication/Azienda1/frigo1", sub2], 1])

    # thread_start([client1, devices[0], "raspberry", "Pieroangela0", conn, "customer/Azienda1/frigo",
    #             "comunication/Azienda1/frigo", sub1], 2)
    th1.start()
    th2.start()
    th1.join()
    print("th1 ended")
    th2.join()
    print("th2 ended")
    print(time.time() - start)
