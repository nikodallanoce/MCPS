import paho.mqtt.client as mqtt


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc, prot):
    if rc == 0:
        print("Connected successfully")
    else:
        print("Connect returned result code: " + str(rc))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("Received message: " + msg.topic + " -> " + msg.payload.decode("utf-8"))


if __name__ == '__main__':
    # create the client
    client = mqtt.Client(protocol=mqtt.MQTTv5)
    client.on_connect = on_connect
    client.on_message = on_message

    # enable TLS
    client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)

    # set username and password
    client.username_pw_set("simplesub", "Simplesub0")

    # connect to HiveMQ Cloud on port 8883
    client.connect("37c7a072139e48e380bb5e3df6662706.s1.eu.hivemq.cloud", 8883, clean_start=False)

    # subscribe to the topic "my/test/topic"
    client.subscribe("my/test/topic", qos=2)  # client.unsubscribe("my/test/topic")

    # Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
    client.loop_forever()
