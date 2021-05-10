import threading
import time
from adafruit_dht import DHT22
import board

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
    conn = "connection_string"
    start = time.time()

    th1 = threading.Thread(target=thread_start,
                           args=[[client1, devices[0], "username1", "password1", conn, "customer/Azienda1/frigo",
                                  "comunication/Azienda1/frigo", sub1], 100])
    th2 = threading.Thread(target=thread_start,
                           args=[[client2, devices[1], "username2", "password2", conn, "customer/Azienda1/frigo1",
                                  "comunication/Azienda1/frigo1", sub2], 100])


    th1.start()
    th2.start()
    th1.join()
    print("th1 ended")
    th2.join()
    print("th2 ended")
    print(time.time() - start)
