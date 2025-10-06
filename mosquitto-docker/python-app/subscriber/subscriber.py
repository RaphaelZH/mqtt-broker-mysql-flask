import paho.mqtt.client as mqtt

import json
import os
import time

broker_host = os.getenv("MQTT_BROKER_HOST", "mqtt-broker")
broker_port = int(os.getenv("MQTT_BROKER_PORT", 1883))


def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("heart_rate/topic")
    client.on_message = handle_telemetry


def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()} on topic {message.topic}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_host, broker_port, 60)

client.loop_start()

while True:
    time.sleep(5)
