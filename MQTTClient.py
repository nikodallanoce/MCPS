import paho.mqtt.client as mqtt
import time


class MQTTClient:

    def __init__(self, identifier: str):
        self.identifier = identifier
        self.client = mqtt.Client(client_id=identifier, protocol=mqtt.MQTTv5)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message_sleep
        self.client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)

    def publish(self, topic: str, payload: str, qos=1):
        self.client.publish(topic, payload, qos=qos)
        time.sleep(1)

    def subscribe(self, topic: str):
        # subscribe to the topic "my/test/topic"
        self.client.subscribe(topic, qos=2)  # client.unsubscribe("my/test/topic")
        # Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
        self.client.loop_forever()

    def unsubscribe(self, topic: str):
        self.client.unsubscribe(topic)

    def disconnect(self):
        self.client.disconnect()

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc, prot):
        if rc == 0:
            print("Connected successfully")
        else:
            print("Connect returned result code: " + str(rc))

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        print("Received message: " + msg.topic + " -> " + payload)
        self.disconnect()

    # The callback for when a PUBLISH message is received from the server.
    def on_message_sleep(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        print("Received message: " + msg.topic + " -> " + payload)
        if "comunication/" in msg.topic:
            time.sleep(float(payload)*60)
        self.disconnect()

    def connect(self, user: str, passwd: str, conn_str: str, clean_start=False):
        # set username and password
        self.client.username_pw_set(user, passwd)
        # connect to HiveMQ Cloud on port 8883
        self.client.connect(conn_str, 8883, clean_start=clean_start)
