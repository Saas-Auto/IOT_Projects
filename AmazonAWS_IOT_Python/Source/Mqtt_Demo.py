#!/usr/bin/python3

#required libraries
import sys
import ssl
import paho.mqtt.client as mqtt
import json
import time

#called while client tries to establish connection with the server
def on_connect(mqttc, obj, flags, rc):
    if rc==0:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: successful")
    elif rc==1:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: Connection refused")

#called when a topic is successfully subscribed to
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos)+"data"+str(obj))

#called when a message is received by a topic
def on_message(mqttc, obj, msg):
    print("Received message from topic: "+msg.topic+" | QoS: "+str(msg.qos)+" | Data Received: "+str(msg.payload))

#creating a client with client-id=mqtt-test
mqttc = mqtt.Client(client_id="WindowsPC")

mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message

#Configure network encryption and authentication options. Enables SSL/TLS support.
#adding client-side certificates and enabling tlsv1.2 support as required by aws-iot service

mqttc.tls_set("./Root-CA.crt",
			certfile="./xxxxxxxxxx-certificate.pem.crt", #rename to correct certificate file name
			keyfile="./xxxxxxxxxx-private.pem.key", #rename to correct key file name
			tls_version=ssl.PROTOCOL_TLSv1_2,
			ciphers=None)

#connecting to aws-account-specific-iot-endpoint
mqttc.connect("xxxxxxxxxx.amazonaws.com", port=8883) #rename to correct host name

time.sleep(5)

#the topic to publish to
mqttc.subscribe("$aws/things/WindowsPC/shadow/get", qos=1) #The names of these topics start with $aws/things/thingName/shadow."

thing = "WindowsPC"
payload = json.dumps({
    "state": {
        "reported": {
            "this_thing_is_alive": True
        }
    }
})

#automatically handles reconnecting
mqttc.loop_start()

while 1==1:
	time.sleep(0.5)
	mqttc.publish("$aws/things/WindowsPC/shadow/update", payload)