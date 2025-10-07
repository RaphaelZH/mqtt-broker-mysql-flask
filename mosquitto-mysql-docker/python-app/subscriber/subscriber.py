from unittest import result
import paho.mqtt.client as mqtt

import mysql.connector

from flask import Flask, render_template

import json
import os
import time

app = Flask(__name__)

# Get MQTT broker credentials from environment variables
MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST")
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT"))

# Get database credentials from environment variables
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")


def handle_telemetry(client, userdata, message):
    global heart_rate
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    sql = "INSERT INTO heartbeat_records (datetime, heart_rate) VALUES (%s, %s)"
    val = (payload["datetime"], payload["heart_rate"])
    my_cursor.execute(sql, val)
    print(my_cursor.rowcount, "record inserted.")


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("heart_rate/topic")
    client.on_message = handle_telemetry


def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()} on topic {message.topic}")


def connect_to_mysql():
    try:
        return mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            port=3306,
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None


@app.route("/", methods=["GET", "POST"])
def index():
    stop = 0
    my_cursor.execute(
        "SELECT heart_rate FROM heartbeat_records ORDER BY datetime DESC LIMIT 1;"
    )
    result = my_cursor.fetchone()
    return render_template(
        "index.html", title="Heartbeat Monitor", heart_rate=result[0], stop=stop
    )


if __name__ == "__main__":
    if db_connection := connect_to_mysql():
        print("Successfully connected to MySQL!")
    else:
        print("Failed to connect to MySQL.")

    db_connection = connect_to_mysql()
    db_connection.autocommit = True
    my_cursor = db_connection.cursor()
    my_cursor.execute(
        "CREATE TABLE IF NOT EXISTS heartbeat_records (datetime VARCHAR(255), heart_rate INT)"
    )
    db_connection.database = "heartbeat_monitor"
    db_connection.table = "heartbeat_records"
    print("Database and table set.")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)

    client.loop_start()

    app.run(host="0.0.0.0", port=5000, debug=True)

    while True:
        time.sleep(5)


# Execute the CREATE DATABASE IF NOT EXISTS statement
# sql_query = "CREATE DATABASE IF NOT EXISTS heartbeat_monitor"
# mycursor.execute(sql_query)
# mydb.database = "heartbeat_monitor"
#
# mycursor.execute(
#    "CREATE TABLE IF NOT EXISTS heartbeat_records (datetime VARCHAR(255), heart_rate INT)"
# )
# mycursor.execute("DROP TABLE IF EXISTS iot_devices")
# mycursor.execute("SHOW TABLES")
# for x in mycursor:
#    print(x)
#    mycursor.execute("SHOW COLUMNS FROM heartbeat_records")
#    for col in mycursor:
#        print("Column:", col)
