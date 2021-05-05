import adafruit_dht
from adafruit_dht import DHT22
import board
import time

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


if __name__ == '__main__':
    devices = [DHT22(board.D4, False), DHT22(board.D18, False)]

    # th = measure(devices[0])
    sensor1, sensor2 = MQTTClient("sensor1"), MQTTClient("sensor2")
    sensor1.connect("raspberry", "Pieroangela0", "37c7a072139e48e380bb5e3df6662706.s1.eu.hivemq.cloud", True)
    sensor2.connect("raspberry2", "Raspberry2", "37c7a072139e48e380bb5e3df6662706.s1.eu.hivemq.cloud", True)

    sensor1.publish("Azienda1/frigo", measure(devices[0]))
    sensor2.publish("Azienda1/frigo1", measure(devices[1]))
    sensor1.disconnect()
    sensor2.disconnect()

    sensor1, sensor2 = MQTTClient("sensor1sub"), MQTTClient("sensor2sub")
    sensor1.connect("raspberry", "Pieroangela0", "37c7a072139e48e380bb5e3df6662706.s1.eu.hivemq.cloud", False)
    sensor2.connect("raspberry2", "Raspberry2", "37c7a072139e48e380bb5e3df6662706.s1.eu.hivemq.cloud", False)
    sensor1.subscribe("comunication/Azienda1/frigo")
    sensor2.subscribe("comunication/Azienda1/frigo1")
