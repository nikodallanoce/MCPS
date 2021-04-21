import paho.mqtt.client as mqtt

if __name__ == '__main__':
    c = mqtt.Client("rasp")
    c.connect(host='192.168.1.48')
    c.publish("home/testing", payload="hello world")
