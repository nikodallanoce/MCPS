import adafruit_dht
from adafruit_dht import DHT22
import board
import time

if __name__ == '__main__':
    devices = [DHT22(board.D4, False), DHT22(board.D18, False)]
    temp_hum = []
    read_correctly = False
    for i in range(2):
        for i in range(len(devices)):
            while not read_correctly:
                try:
                    t, h = devices[i].temperature, devices[i].humidity
                    read_correctly = True
                    #print("Temp={0:0.1f}'C, Humidity={1:0.1f}%".format(t, h))
                    print("Dev {0} -> temp: {1}'C ___ hum: {2}%".format(i, t, h))
                except RuntimeError as error:
                    # Errors happen fairly often, DHT's are hard to read, just keep going
                    print("Dev {0} -> {1}".format(i, error.args[0]))
                    time.sleep(3.0)
                except Exception as error:
                    devices[i].exit()
                    raise error
            read_correctly = False
        time.sleep(2)


