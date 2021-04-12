import adafruit_dht
import board
import time

if __name__ == '__main__':
    dhtDevice = adafruit_dht.DHT22(board.D4, False)
    read_correctly = False
    for i in range(5):
        while not read_correctly:
            try:
                t, h = dhtDevice.temperature, dhtDevice.humidity
                read_correctly = True
                print("Temp={0:0.1f}'C ---- Humidity={1:0.1f}%".format(t, h))
                time.sleep(5.0)

            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                print(error.args[0])
                time.sleep(2.0)
            except Exception as error:
                dhtDevice.exit()
                raise error

        read_correctly = False
