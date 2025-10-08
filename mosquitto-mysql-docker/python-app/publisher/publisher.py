import paho.mqtt.client as mqtt

import json
import os
import time

broker_host = os.getenv("MQTT_BROKER_HOST", "mqtt-broker")
broker_port = int(os.getenv("MQTT_BROKER_PORT", 1883))


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("heart_rate/topic")


def random_heart_rate():
    return 60 + int(40 * os.urandom(1)[0] / 255)  # Random heart rate between 60 and 100


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect

client.connect(broker_host, broker_port, 60)

client.loop_start()

while True:
    heart_rate = random_heart_rate()
    telemetry = json.dumps(
        {"datetime": time.strftime("%Y-%m-%d %H:%M:%S"), "heart_rate": heart_rate}
    )
    print(f"Publishing heart rate: {heart_rate}")
    print("Sending telemetry: ", telemetry)
    client.publish("heart_rate/topic", telemetry)
    time.sleep(2)
