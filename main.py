import paho.mqtt.client as mqtt

if __name__ == '__main__':
    c = mqtt.Client("rasp", protocol=mqtt.MQTTv5)
    c.username_pw_set("rasp", "pieroangela")
    c.connect(host='node02.myqtthub.com', clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY)
    #c.subscribe("home/testing")
    c.publish("home/testing", payload="hello world")
