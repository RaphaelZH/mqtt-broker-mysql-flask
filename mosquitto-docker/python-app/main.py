import paho.mqtt.client as mqtt
import os
import time

broker_host = os.getenv("MQTT_BROKER_HOST", "mqtt-broker")
broker_port = int(os.getenv("MQTT_BROKER_PORT", 1883))

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("test/topic")

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_host, broker_port, 60)

client.loop_start()

# Example: Publish a message
while True:
    client.publish("test/topic", "Hello from Python!")
    time.sleep(5)